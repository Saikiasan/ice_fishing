import os
import sys
import json
import time
import asyncio
import threading
import mimetypes
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import websockets

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTTP_PORT = 8088
WS_PORT = 8765

# Ensure MIME types
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("audio/webm", ".webm")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/json", ".json")

# 53 Sectors sequence for Evolution Ice Fishing
WHEEL_SECTORS = []
for i in range(53):
    if i == 0:
        WHEEL_SECTORS.append("HugeReds")
    elif i in [13, 39]:
        WHEEL_SECTORS.append("BigOranges")
    elif i in [6, 20, 33, 46]:
        WHEEL_SECTORS.append("LilBlues")
    else:
        WHEEL_SECTORS.append("Leaf1" if i % 2 == 1 else "Leaf2")

PAYOUT_TABLE = {
    "Leaf1": 2.0,       # Pays 1:1 (+ stake back = 2x)
    "Leaf2": 2.0,       # Pays 1:1 (+ stake back = 2x)
    "LilBlues": 4.0,    # Pays 3:1 (+ stake back = 4x)
    "BigOranges": 6.0,  # Pays 5:1 (+ stake back = 6x)
    "HugeReds": 11.0    # Pays 10:1 (+ stake back = 11x)
}

# Real-Play Game State & Persistent Balance
DEFAULT_INITIAL_BALANCE = 50000.0
try:
    if len(sys.argv) > 1:
        DEFAULT_INITIAL_BALANCE = float(sys.argv[1])
except Exception:
    pass

game_control_state = {
    "initial_balance": DEFAULT_INITIAL_BALANCE,
    "balance": DEFAULT_INITIAL_BALANCE,
    "committed_balance": DEFAULT_INITIAL_BALANCE,  # Balance before bets in active round
    "current_bets": {},
    "last_bets": {},
    "version": 1,
    "forced_next_outcome": None,  # Can be dict: {"result": "LilBlues", "multiplier": 4} or None
}

# Running Spin History List (index 0 is newest)
spin_history_list = [
    {"result": "Leaf1", "wheelMultiplier": {"value": 4, "level": "Low"}},
    {"result": "Leaf2"}, {"result": "LilBlues"}, {"result": "Leaf1"},
    {"result": "BigOranges"}, {"result": "Leaf2"}, {"result": "Leaf1"},
    {"result": "HugeReds"}, {"result": "Leaf1"}, {"result": "Leaf2"}
]

connected_clients = set()

def make_balance_payload(bal):
    game_control_state["version"] += 1
    v = game_control_state["version"]
    return {
        "balance": float(bal),
        "currency": "INR",
        "tableId": "IceFishing000001",
        "balances": [
            {
                "id": "combined",
                "amount": float(bal),
                "version": v,
                "currency": "INR",
                "serverBalance": float(bal),
                "serverBalanceVersion": v,
                "activeBalanceId": "combined"
            },
            {
                "id": "IceFishing000001",
                "amount": float(bal),
                "version": v,
                "currency": "INR",
                "serverBalance": float(bal),
                "serverBalanceVersion": v,
                "activeBalanceId": "combined"
            },
            {
                "id": "main",
                "amount": float(bal),
                "version": v,
                "currency": "INR",
                "serverBalance": float(bal),
                "serverBalanceVersion": v,
                "activeBalanceId": "combined"
            }
        ]
    }

async def broadcast(data):
    if not connected_clients:
        return
    if isinstance(data, dict) and "time" not in data:
        data["time"] = int(time.time() * 1000)
    payload = json.dumps(data)
    for ws in list(connected_clients):
        try:
            await ws.send(payload)
        except Exception:
            pass

# Custom HTTP Request Handler for Evolution Production Endpoints & Admin Control API
class EvoHTTPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        path = self.path.split("?")[0]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        
        # API: Set Next Outcome
        if path == "/api/set_next_outcome":
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
                target_result = data.get("result") # Leaf1, Leaf2, LilBlues, BigOranges, HugeReds
                multiplier = data.get("multiplier", 1)
                if target_result:
                    mult_val = "random" if str(multiplier).lower() == "random" else (int(multiplier) if multiplier else 1)
                    game_control_state["forced_next_outcome"] = {
                        "result": target_result,
                        "multiplier": mult_val
                    }
                    print(f"\n[ADMIN] Next round FORCED to: {game_control_state['forced_next_outcome']}\n")
                    self.send_json_response({"status": "ok", "forced_next_outcome": game_control_state["forced_next_outcome"]})
                else:
                    game_control_state["forced_next_outcome"] = None
                    print(f"\n[ADMIN] Cleared forced outcome. Back to random.\n")
                    self.send_json_response({"status": "ok", "forced_next_outcome": None})
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, 400)
            return

        # API: Set Balance
        if path == "/api/set_balance":
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
                new_bal = float(data.get("balance", DEFAULT_INITIAL_BALANCE))
                game_control_state["balance"] = new_bal
                game_control_state["committed_balance"] = new_bal
                print(f"\n[ADMIN] Player balance reset to: ₹{new_bal}\n")
                
                # Schedule WebSocket broadcast of new balance
                asyncio.run_coroutine_threadsafe(
                    broadcast({
                        "type": "balanceUpdated",
                        "payload": make_balance_payload(new_bal),
                        "args": make_balance_payload(new_bal)
                    }),
                    main_loop
                )
                self.send_json_response({"status": "ok", "balance": new_bal})
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, 400)
            return

        # Print client log messages for debugging
        if path.startswith("/log"):
            try:
                log_json = json.loads(body.decode("utf-8")) if body else {}
                print(f"[CLIENT_LOG] {log_json}", flush=True)
            except Exception as e:
                print(f"[CLIENT_LOG_ERR] {body[:200]}", flush=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        # Handle Evolution logs and metrics silently
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path
        query = urllib.parse.parse_qs(url_parts.query)
        base_dir = os.path.join(os.path.dirname(__file__), "evo_server")

        # Root Redirect to Official Evolution Ice Fishing client
        if path in ["/", "/index.html"]:
            self.send_response(302)
            self.send_header("Location", "/frontend/evo/r3/index.html#table_id=IceFishing000001&game=icefishing&preload_app=skipper.V0")
            self.end_headers()
            return

        # API: Query or GET set outcome (easy via browser URL bar)
        # e.g.: /api/outcome?result=LilBlues&mult=4 or /api/outcome?result=BigOranges&mult=random
        if path == "/api/outcome":
            target = query.get("result", [None])[0]
            mult = query.get("mult", [1])[0]
            if target:
                mult_val = "random" if str(mult).lower() == "random" else int(mult)
                game_control_state["forced_next_outcome"] = {
                    "result": target,
                    "multiplier": mult_val
                }
                print(f"\n[ADMIN GET] Next round FORCED to: {game_control_state['forced_next_outcome']}\n")
            elif "clear" in query:
                game_control_state["forced_next_outcome"] = None
                print(f"\n[ADMIN GET] Cleared forced outcome.\n")
            self.send_json_response({
                "forced_next_outcome": game_control_state["forced_next_outcome"],
                "balance": game_control_state["balance"],
                "active_bets": game_control_state["current_bets"]
            })
            return

        # API: Query or GET set balance (easy via browser URL bar)
        # e.g.: /api/balance?amount=100000
        if path == "/api/balance":
            amt_str = query.get("amount", [None])[0]
            if amt_str:
                new_bal = float(amt_str)
                game_control_state["balance"] = new_bal
                game_control_state["committed_balance"] = new_bal
                print(f"\n[ADMIN GET] Balance set to: ₹{new_bal}\n")
                asyncio.run_coroutine_threadsafe(
                    broadcast({
                        "type": "balanceUpdated",
                        "payload": make_balance_payload(new_bal),
                        "args": make_balance_payload(new_bal)
                    }),
                    main_loop
                )
                asyncio.run_coroutine_threadsafe(
                    broadcast({
                        "type": "icefishing.bets",
                        "payload": {
                            "state": {
                                "status": "NoBets",
                                "balance": float(new_bal),
                                "chips": {},
                                "repeat": game_control_state["last_bets"],
                                "history": []
                            }
                        }
                    }),
                    main_loop
                )
            self.send_json_response({
                "balance": game_control_state["balance"],
                "committed_balance": game_control_state["committed_balance"],
                "forced_next_outcome": game_control_state["forced_next_outcome"]
            })
            return

        # API: Setup
        if path == "/setup":
            self.serve_json(os.path.join(base_dir, "setup.json"))
            return

        # API: Style
        if path == "/style":
            self.serve_json(os.path.join(base_dir, "style.json"))
            return

        # API: Config
        if path == "/config":
            config_file = os.path.join(base_dir, "config.json")
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f_cfg:
                    cfg = json.load(f_cfg)
                # Dynamically set host and wsUrl based on the incoming request Host header
                req_host = self.headers.get("Host", f"127.0.0.1:{HTTP_PORT}").split(":")[0]
                cfg["serverHost"] = f"{req_host}:{HTTP_PORT}"
                cfg["wsUrl"] = f"ws://{req_host}:{WS_PORT}"
                data = json.dumps(cfg, indent=2).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(data)
                return
            self.serve_json(config_file)
            return

        # API: Player screenName
        if path == "/api/player/screenName":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"screenName":"IceHunter"}')
            return

        # API: Snapshots or bonus claims
        if path.startswith("/public/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"snapshots":[],"unclaimed":[]}')
            return

        # API: Video settings.xml
        if path == "/player/games/assets/settings.xml":
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.end_headers()
            self.wfile.write(b'<settings><video auto="true"/></settings>')
            return

        # Static frontend files under /frontend/...
        if path.startswith("/frontend/"):
            rel_path = path.lstrip("/")
            local_path = os.path.join(base_dir, rel_path)
            if os.path.exists(local_path) and not os.path.isdir(local_path):
                self.serve_file(local_path)
                return

        # Fallback to default SimpleHTTPRequestHandler
        super().do_GET()

    def send_json_response(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(data)

    def serve_json(self, filepath):
        if not os.path.exists(filepath):
            self.send_error(404, "File not found")
            return
        with open(filepath, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(data)

    def serve_file(self, filepath):
        mime, _ = mimetypes.guess_type(filepath)
        if not mime:
            mime = "application/octet-stream"
        with open(filepath, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(data)


# Real-Time WebSocket Game Engine Handler
async def ws_handler(websocket):
    print(f"[WS] Client connected: {websocket.remote_address}")
    connected_clients.add(websocket)

    # 1. Immediate balance notification reflecting persistent real-play balance
    b_data = make_balance_payload(game_control_state["balance"])
    await websocket.send(json.dumps({
        "type": "balanceUpdated",
        "payload": b_data,
        "args": b_data,
        "time": int(time.time() * 1000)
    }))

    # 2. Table state
    table_state = {
        "tableId": "IceFishing000001",
        "game": "icefishing"
    }
    await websocket.send(json.dumps({
        "type": "tableState",
        "payload": table_state,
        "args": table_state,
        "time": int(time.time() * 1000)
    }))

    # 3. Table initialization (layout, current game, dealer)
    table_payload = {
        "wheel": {
            "layout": WHEEL_SECTORS,
            "spin": {
                "direction": "Clockwise",
                "sector": 1
            }
        },
        "currentGame": {
            "gameId": "18dec100001a2c4ca24a8d4",
            "gameNumber": time.strftime("%H:%M:%S")
        },
        "dealer": {
            "screenName": "Emma"
        }
    }
    await websocket.send(json.dumps({
        "type": "icefishing.table",
        "payload": table_payload,
        "args": table_payload,
        "time": int(time.time() * 1000)
    }))

    # 4. Initial history payload
    history_payload = {
        "results": list(spin_history_list)
    }
    await websocket.send(json.dumps({
        "type": "icefishing.spinHistory",
        "payload": history_payload,
        "args": history_payload,
        "time": int(time.time() * 1000)
    }))

    try:
        async for msg in websocket:
            try:
                data = json.loads(msg)
                outer_id = data.get("id")
                recipient = data.get("recipient")
                payload = data.get("payload") if isinstance(data.get("payload"), dict) else data
                inner_id = payload.get("id") if isinstance(payload, dict) else None
                msg_type = payload.get("type") or data.get("type")
                if msg_type not in ["metrics.ping", "ping"]:
                    print(f"[WS INCOMING] type={msg_type} recipient={recipient} payload={payload}")

                reply_ids = [i for i in [outer_id, inner_id] if i]

                # 1. Handle fetchBalance / balance request
                if msg_type == "fetchBalance" or recipient == "balance":
                    b_data = make_balance_payload(game_control_state["balance"])
                    for rid in reply_ids:
                        await websocket.send(json.dumps({
                            "type": "balanceUpdated",
                            "replyToId": rid,
                            "replyTo": rid,
                            "payload": b_data,
                            "args": b_data,
                            "time": int(time.time() * 1000)
                        }))
                    await websocket.send(json.dumps({
                        "type": "balanceUpdated",
                        "payload": b_data,
                        "args": b_data,
                        "time": int(time.time() * 1000)
                    }))

                # 2. Handle bet placement: icefishing.placeChips
                elif msg_type == "icefishing.placeChips":
                    args = payload.get("args") if isinstance(payload.get("args"), dict) else {}
                    incoming_chips = (
                        args.get("chips") or
                        args.get("bet") or
                        payload.get("chips") or
                        payload.get("bet") or
                        data.get("args", {}).get("chips") or
                        data.get("args", {}).get("bet") or
                        {}
                    )
                    if not incoming_chips and isinstance(payload, dict):
                        for k, v in payload.items():
                            if k in ["Leaf1", "Leaf2", "LilBlues", "BigOranges", "HugeReds"]:
                                incoming_chips[k] = v

                    for bet_spot, amt in incoming_chips.items():
                        game_control_state["current_bets"][bet_spot] = amt

                    total_bet = sum(game_control_state["current_bets"].values())
                    # Dynamic balance deduction from committed_balance
                    game_control_state["balance"] = max(0.0, game_control_state["committed_balance"] - total_bet)
                    print(f"[BET RECEIVED] Active Bets: {game_control_state['current_bets']} | Total Bet: ₹{total_bet} | Live Balance: ₹{game_control_state['balance']}")

                    bets_ack = {
                        "state": {
                            "status": "Accepted",
                            "balance": float(game_control_state["balance"]),
                            "chips": game_control_state["current_bets"],
                            "repeat": game_control_state["current_bets"],
                            "invalidBets": {},
                            "history": [{"action": "Place", "chips": game_control_state["current_bets"]}]
                        }
                    }
                    await websocket.send(json.dumps({
                        "type": "icefishing.bets",
                        "payload": bets_ack,
                        "args": bets_ack,
                        "time": int(time.time() * 1000)
                    }))

                    b_data = make_balance_payload(game_control_state["balance"])
                    await websocket.send(json.dumps({
                        "type": "balanceUpdated",
                        "payload": b_data,
                        "args": b_data,
                        "time": int(time.time() * 1000)
                    }))

                # 3. Handle Undo
                elif msg_type in ["icefishing.undo", "icefishing.undoAll"]:
                    game_control_state["current_bets"].clear()
                    # Restore balance back to committed_balance of this round
                    game_control_state["balance"] = game_control_state["committed_balance"]
                    print(f"[BET UNDO] Bets cleared. Balance restored to: ₹{game_control_state['balance']}")
                    bets_ack = {
                        "state": {
                            "status": "NoBets",
                            "balance": float(game_control_state["balance"]),
                            "chips": {},
                            "repeat": {},
                            "invalidBets": {},
                            "history": []
                        }
                    }
                    await websocket.send(json.dumps({
                        "type": "icefishing.bets",
                        "payload": bets_ack,
                        "args": bets_ack,
                        "time": int(time.time() * 1000)
                    }))
                    b_data = make_balance_payload(game_control_state["balance"])
                    await websocket.send(json.dumps({
                        "type": "balanceUpdated",
                        "payload": b_data,
                        "args": b_data,
                        "time": int(time.time() * 1000)
                    }))

                # 4. Handle settings.read request
                elif msg_type == "settings.read" or recipient == "player-settings":
                    s_data = {"data": []}
                    for rid in reply_ids:
                        await websocket.send(json.dumps({
                            "type": "settings.read.reply",
                            "replyToId": rid,
                            "replyTo": rid,
                            "payload": s_data,
                            "args": s_data,
                            "time": int(time.time() * 1000)
                        }))

                # 5. Handle metrics.ping / ping
                elif "ping" in str(msg_type):
                    p_data = {"t": time.time()}
                    for rid in reply_ids:
                        await websocket.send(json.dumps({
                            "type": "metrics.pong",
                            "replyToId": rid,
                            "replyTo": rid,
                            "payload": p_data,
                            "args": p_data,
                            "time": int(time.time() * 1000)
                        }))

                # 6. Generic reply for other messages
                else:
                    for rid in reply_ids:
                        await websocket.send(json.dumps({
                            "type": f"{msg_type}.reply",
                            "replyToId": rid,
                            "replyTo": rid,
                            "payload": {},
                            "args": {},
                            "time": int(time.time() * 1000)
                        }))

            except Exception as e:
                print(f"[WS ERR] {e}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"[WS] Client disconnected")

# Evolution Game State Machine with Real-Play Win-Loss Balance & Outcome Control
async def broadcast_game_loop():
    round_id = 100
    import random

    while True:
        round_id += 1
        game_num = time.strftime("%H:%M:%S")
        game_id = f"18dec{round_id:06x}a2c4ca24a8d4"
        start_sector = random.randint(0, 52)
        direction = "Clockwise" if random.random() > 0.5 else "Counterclockwise"

        # Baseline committed balance at round start
        game_control_state["committed_balance"] = game_control_state["balance"]

        # 1. betsOpen (8 seconds)
        print(f"\n========================================================")
        print(f"[ROUND #{round_id} START] Time: {game_num} | Player Funds: ₹{game_control_state['balance']:.2f}")
        if game_control_state["forced_next_outcome"]:
            print(f"[PRESET ACTIVE] Outcome preset: {game_control_state['forced_next_outcome']}")
        print(f"========================================================")

        bets_open_payload = {
            "gameId": game_id,
            "gameNumber": game_num,
            "timeRemaining": 8000,
            "spinInfo": {
                "sector": start_sector + 1,
                "speed": "Medium",
                "direction": direction
            }
        }
        await broadcast({
            "type": "icefishing.betsOpen",
            "payload": bets_open_payload,
            "args": bets_open_payload
        })
        await asyncio.sleep(8.0)

        # 2. betsClosed
        print(f"[PHASE] betsClosed")
        bets_closed_payload = {
            "gameNumber": game_num
        }
        await broadcast({
            "type": "icefishing.betsClosed",
            "payload": bets_closed_payload,
            "args": bets_closed_payload
        })
        await asyncio.sleep(1.5)

        # Determine Winning Outcome (Preset outcome if configured, otherwise random)
        forced = game_control_state["forced_next_outcome"]
        game_control_state["forced_next_outcome"] = None  # Consume one-shot preset

        if forced and forced.get("result"):
            target_res = forced["result"]
            matching_indices = [idx for idx, sec in enumerate(WHEEL_SECTORS) if sec.lower() == target_res.lower()]
            if matching_indices:
                winning_sector = random.choice(matching_indices)
            else:
                winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            f_mult = forced.get("multiplier", 1)
            if str(f_mult).lower() == "random" or (int(f_mult) <= 1 and winning_result in ["LilBlues", "BigOranges", "HugeReds"]):
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = int(f_mult)
        else:
            winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            # If a fish is caught, always assign a multiplier!
            if winning_result in ["LilBlues", "BigOranges", "HugeReds"]:
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = 1

        # 3. wheelSpinning with multipliers
        multipliers = {}
        # If target multiplier specified, assign it to winning sector
        if target_mult > 1:
            multipliers[str(winning_sector + 1)] = {
                "result": winning_result,
                "multiplier": {"value": target_mult, "level": "High" if target_mult >= 10 else "Low"}
            }

        # Add 1 to 2 random filler multipliers on other sectors
        filler_count = random.randint(1, 2)
        for _ in range(filler_count):
            sec = random.randint(0, 52)
            if sec != winning_sector:
                val = random.choice([2, 3, 4, 5, 7, 10, 25])
                multipliers[str(sec + 1)] = {
                    "result": WHEEL_SECTORS[sec],
                    "multiplier": {"value": val, "level": "High" if val >= 10 else "Low"}
                }

        print(f"[PHASE] wheelSpinning (Assigned {len(multipliers)} multipliers)")
        spinning_payload = {
            "leafWheelMultipliers": multipliers,
            "bonusWheelMultipliers": {}
        }
        await broadcast({
            "type": "icefishing.wheelSpinning",
            "payload": spinning_payload,
            "args": spinning_payload
        })
        await asyncio.sleep(3.5)

        # 4. wheelStopping (4 seconds deceleration advance signal)
        print(f"[PHASE] wheelStopping -> Declared Sector: {winning_sector+1} ({winning_result})")
        stopping_payload = {
            "sector": winning_sector + 1,
            "timeRemaining": 4000,
            "gameNumber": game_num,
            "gameId": game_id,
            "leafWheelMultipliers": multipliers,
            "bonusWheelMultipliers": {}
        }
        await broadcast({
            "type": "icefishing.wheelStopping",
            "payload": stopping_payload,
            "args": stopping_payload
        })
        await asyncio.sleep(4.0)

        # 5. wheelResult
        print(f"[PHASE] wheelResult -> {winning_result}")
        result_payload = {
            "result": winning_result,
            "leafWheelMultipliers": multipliers,
            "bonusWheelMultipliers": {}
        }
        await broadcast({
            "type": "icefishing.wheelResult",
            "payload": result_payload,
            "args": result_payload
        })

        # Calculate multiplier for winning sector
        total_mult = 1
        sec_key = str(winning_sector + 1)
        if sec_key in multipliers:
            total_mult = multipliers[sec_key]["multiplier"]["value"]

        # Append outcome to live running history
        new_spin_record = {"result": winning_result}
        if total_mult > 1:
            new_spin_record["wheelMultiplier"] = {
                "value": total_mult,
                "level": "High" if total_mult >= 10 else "Low"
            }

        spin_history_list.insert(0, new_spin_record)
        if len(spin_history_list) > 75:
            spin_history_list.pop()

        # Dynamic bead shift
        history_update = {
            "newResult": True,
            "results": [new_spin_record]
        }
        await broadcast({
            "type": "icefishing.spinHistory",
            "payload": history_update,
            "args": history_update
        })

        await asyncio.sleep(1.5)

        # 6. Real-Play Settlement & Balance Persistence
        # Check if user had bet on the winning outcome
        active_bets = game_control_state["current_bets"]
        user_bet_amount = active_bets.get(winning_result, 0)
        payout = 0.0

        if user_bet_amount > 0:
            base_payout = PAYOUT_TABLE.get(winning_result, 2.0)
            payout = user_bet_amount * base_payout * (total_mult if total_mult > 1 else 1.0)
            # Add win directly to running balance
            game_control_state["balance"] += payout
            print(f"[ROUND RESULT: WIN!] Outcome: {winning_result} (x{total_mult}) | Bet: ₹{user_bet_amount} -> Paid: ₹{payout} | Persistent Balance: ₹{game_control_state['balance']:.2f}")
        else:
            total_wager = sum(active_bets.values())
            if total_wager > 0:
                print(f"[ROUND RESULT: LOSS] Outcome: {winning_result} | Lost Wager: ₹{total_wager} | Persistent Balance: ₹{game_control_state['balance']:.2f}")
            else:
                print(f"[ROUND RESULT: NO BET] Outcome: {winning_result} | Persistent Balance: ₹{game_control_state['balance']:.2f}")

        # Broadcast live updated real-play balance
        game_control_state["committed_balance"] = game_control_state["balance"]
        await broadcast({
            "type": "balanceUpdated",
            "payload": make_balance_payload(game_control_state["balance"]),
            "args": make_balance_payload(game_control_state["balance"])
        })

        # Broadcast Settled status to Evolution client so YouWin popup & winning chip animation trigger
        settled_accepted_bets = {}
        for spot, amt in active_bets.items():
            settled_accepted_bets[spot] = {
                "amount": float(amt),
                "payout": float(payout) if spot == winning_result else 0.0
            }

        win_level = "None"
        if payout > 0:
            ratio = payout / max(1.0, user_bet_amount)
            if ratio >= 10:
                win_level = "Big"
            elif ratio >= 4:
                win_level = "Medium"
            else:
                win_level = "Small"

        settled_payload = {
            "state": {
                "status": "Settled",
                "winType": win_level,
                "totalPayout": float(payout),
                "balance": float(game_control_state["balance"]),
                "acceptedBets": settled_accepted_bets,
                "chips": active_bets,
                "repeat": active_bets,
                "invalidBets": {}
            }
        }
        await broadcast({
            "type": "icefishing.bets",
            "payload": settled_payload,
            "args": settled_payload
        })

        resolved_payload = {
            "result": winning_result,
            "totalMultiplier": total_mult,
            "leafWheelMultipliers": multipliers,
            "bonusWheelMultipliers": {}
        }
        await broadcast({
            "type": "icefishing.gameResolved",
            "payload": resolved_payload,
            "args": resolved_payload
        })
        await asyncio.sleep(4.0)

        # 7. gameCleared (Clear active round bets, preserve last_bets for repeat)
        game_control_state["last_bets"] = dict(game_control_state["current_bets"])
        game_control_state["current_bets"].clear()

        await broadcast({
            "type": "icefishing.bets",
            "payload": {
                "state": {
                    "status": "NoBets",
                    "balance": float(game_control_state["balance"]),
                    "chips": {},
                    "repeat": game_control_state["last_bets"],
                    "invalidBets": {},
                    "history": []
                }
            }
        })

        await broadcast({
            "type": "icefishing.gameCleared",
            "payload": {},
            "args": {}
        })
        await asyncio.sleep(1.5)

def start_http_server():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), EvoHTTPHandler)
    print(f"[HTTP] Evolution Production Mirror & API Server on http://0.0.0.0:{HTTP_PORT}")
    server.serve_forever()

main_loop = None

async def main():
    global main_loop
    main_loop = asyncio.get_running_loop()

    # Start HTTP in daemon thread
    t = threading.Thread(target=start_http_server, daemon=True)
    t.start()

    # Start WebSocket Server
    print(f"[WS] Evolution Game WebSocket Server listening on ws://0.0.0.0:{WS_PORT}")
    print(f"[REAL-PLAY] Starting persistent balance: ₹{game_control_state['balance']:.2f}")
    async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
        await broadcast_game_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutdown.")
