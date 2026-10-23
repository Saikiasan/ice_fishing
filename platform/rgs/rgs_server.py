import asyncio
import json
import random
import time
import secrets
from typing import Dict, Set, Any, Optional
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

PLATFORM_CORE_URL = "http://localhost:8000"

app = FastAPI(title="Remote Game Server (RGS) - Ice Fishing Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IceFishingRoundState:
    WAITING_FOR_BETS = "WAITING_FOR_BETS"   # 8 seconds countdown
    FISHING_ACTIVE = "FISHING_ACTIVE"       # 5 seconds line in water
    REVEAL_PAYOUT = "REVEAL_PAYOUT"         # 4 seconds reveal fish & multiplier

# Distinct fish types with realistic RTP math profile
FISH_TIERS = [
    {"type": "Perch", "name": "Small Perch", "mult": 1.2, "weight": 40},
    {"type": "Trout", "name": "Rainbow Trout", "mult": 2.0, "weight": 25},
    {"type": "Pike", "name": "Northern Pike", "mult": 5.0, "weight": 18},
    {"type": "Walleye", "name": "Golden Walleye", "mult": 10.0, "weight": 10},
    {"type": "ArcticChar", "name": "Arctic Char", "mult": 25.0, "weight": 5},
    {"type": "LegendarySturgeon", "name": "King Sturgeon", "mult": 100.0, "weight": 2},
]

class ConnectedPlayer:
    def __init__(self, ws: WebSocket, user_id: int, username: str, balance: float):
        self.ws = ws
        self.user_id = user_id
        self.username = username
        self.balance = balance
        self.active_bet: float = 0.0

class IceFishingGameRoom:
    def __init__(self):
        self.round_id: str = f"round_{secrets.token_hex(6)}"
        self.state: str = IceFishingRoundState.WAITING_FOR_BETS
        self.state_time_left: int = 8
        self.players: Dict[WebSocket, ConnectedPlayer] = {}
        self.round_bets: Dict[int, float] = {}  # user_id -> bet_amount
        self.last_outcome: Optional[Dict[str, Any]] = None

    async def broadcast(self, message: Dict[str, Any]):
        dead = []
        payload = json.dumps(message)
        for ws in self.players.keys():
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            if ws in self.players:
                del self.players[ws]

    def pick_fish_outcome(self) -> Dict[str, Any]:
        """Server-authoritative RNG draw for fish multipliers."""
        # 30% chance of nothing caught / hook snapped
        if random.random() < 0.30:
            return {
                "caught": False,
                "fish": None,
                "multiplier": 0.0,
                "message": "Fish slipped off the hook!"
            }
        
        # Weighted random selection
        total_weight = sum(f["weight"] for f in FISH_TIERS)
        pick = random.uniform(0, total_weight)
        cumulative = 0
        selected = FISH_TIERS[0]
        for fish in FISH_TIERS:
            cumulative += fish["weight"]
            if pick <= cumulative:
                selected = fish
                break
        
        return {
            "caught": True,
            "fish": selected["name"],
            "fish_type": selected["type"],
            "multiplier": selected["mult"],
            "message": f"Hooked a {selected['name']}! ({selected['mult']}x)"
        }

room = IceFishingGameRoom()

async def rgs_core_debit(user_id: int, amount: float, round_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{PLATFORM_CORE_URL}/api/v1/rgs/debit",
                json={"user_id": user_id, "amount": amount, "round_id": round_id, "game_id": "ice_fishing"},
                timeout=5.0
            )
            return res.status_code == 200
        except Exception as e:
            print(f"[RGS ERROR] Debit failed: {e}")
            return False

async def rgs_core_credit(user_id: int, payout: float, round_id: str) -> Optional[float]:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{PLATFORM_CORE_URL}/api/v1/rgs/credit",
                json={"user_id": user_id, "payout": payout, "round_id": round_id, "game_id": "ice_fishing"},
                timeout=5.0
            )
            if res.status_code == 200:
                data = res.json()
                if "transaction" in data:
                    return data["transaction"]["balance_after"]
                return data.get("balance_after")
        except Exception as e:
            print(f"[RGS ERROR] Credit failed: {e}")
    return None

# --- Main Game Loop Background Task ---
async def game_state_loop():
    while True:
        try:
            # 1. WAITING FOR BETS PHASE
            room.round_id = f"round_{secrets.token_hex(6)}"
            room.state = IceFishingRoundState.WAITING_FOR_BETS
            room.round_bets.clear()
            room.last_outcome = None
            
            for countdown in range(8, 0, -1):
                room.state_time_left = countdown
                await room.broadcast({
                    "event": "STATE_UPDATE",
                    "state": room.state,
                    "round_id": room.round_id,
                    "time_left": countdown,
                    "total_bets_count": len(room.round_bets)
                })
                await asyncio.sleep(1)

            # 2. FISHING ACTIVE PHASE (Lures dropped, ice hole active)
            room.state = IceFishingRoundState.FISHING_ACTIVE
            await room.broadcast({
                "event": "STATE_UPDATE",
                "state": room.state,
                "round_id": room.round_id,
                "message": "Line dropped into the ice hole! Waiting for bites..."
            })
            await asyncio.sleep(4)

            # 3. REVEAL & SETTLE PAYOUTS PHASE
            outcome = room.pick_fish_outcome()
            room.last_outcome = outcome
            room.state = IceFishingRoundState.REVEAL_PAYOUT

            # Calculate and credit payouts via Core Platform Ledger
            payout_results = []
            for user_id, bet_amount in room.round_bets.items():
                mult = outcome["multiplier"] if outcome["caught"] else 0.0
                win_amount = round(bet_amount * mult, 2)
                new_bal = None
                if win_amount > 0:
                    new_bal = await rgs_core_credit(user_id, win_amount, room.round_id)
                
                # Update player cached balance if player is in room
                for p in room.players.values():
                    if p.user_id == user_id:
                        if new_bal is not None:
                            p.balance = new_bal
                        payout_results.append({
                            "user_id": user_id,
                            "username": p.username,
                            "bet": bet_amount,
                            "multiplier": mult,
                            "payout": win_amount,
                            "balance": p.balance
                        })

            await room.broadcast({
                "event": "ROUND_RESULT",
                "round_id": room.round_id,
                "state": room.state,
                "outcome": outcome,
                "payouts": payout_results
            })
            await asyncio.sleep(4)

        except Exception as e:
            print(f"[RGS LOOP ERROR] {e}")
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(game_state_loop())

@app.websocket("/ws/ice_fishing")
async def websocket_ice_fishing(websocket: WebSocket, token: Optional[str] = None):
    await websocket.accept()
    if not token:
        await websocket.send_text(json.dumps({"event": "ERROR", "message": "Missing authentication token"}))
        await websocket.close()
        return

    # Verify token against Core Platform
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(f"{PLATFORM_CORE_URL}/api/v1/rgs/verify_token?token={token}")
            if res.status_code != 200:
                await websocket.send_text(json.dumps({"event": "ERROR", "message": "Invalid launch token"}))
                await websocket.close()
                return
            user_data = res.json()
        except Exception as e:
            await websocket.send_text(json.dumps({"event": "ERROR", "message": "Platform handshake failed"}))
            await websocket.close()
            return

    player = ConnectedPlayer(
        ws=websocket,
        user_id=user_data["user_id"],
        username=user_data["username"],
        balance=user_data["balance"]
    )
    room.players[websocket] = player

    # Send initial welcome state
    await websocket.send_text(json.dumps({
        "event": "JOIN_SUCCESS",
        "user_id": player.user_id,
        "username": player.username,
        "balance": player.balance,
        "round_id": room.round_id,
        "state": room.state,
        "time_left": room.state_time_left
    }))

    try:
        while True:
            raw_data = await websocket.receive_text()
            msg = json.loads(raw_data)
            action = msg.get("action")

            if action == "PLACE_BET":
                amount = float(msg.get("amount", 0.0))
                if room.state != IceFishingRoundState.WAITING_FOR_BETS:
                    await websocket.send_text(json.dumps({"event": "BET_ERROR", "message": "Betting is closed for this round"}))
                    continue
                if amount <= 0:
                    await websocket.send_text(json.dumps({"event": "BET_ERROR", "message": "Invalid bet amount"}))
                    continue
                if amount > player.balance:
                    await websocket.send_text(json.dumps({"event": "BET_ERROR", "message": "Insufficient balance"}))
                    continue

                # Debit wallet atomically
                debit_ok = await rgs_core_debit(player.user_id, amount, room.round_id)
                if not debit_ok:
                    await websocket.send_text(json.dumps({"event": "BET_ERROR", "message": "Wallet debit rejected"}))
                    continue

                player.balance = round(player.balance - amount, 2)
                room.round_bets[player.user_id] = round(room.round_bets.get(player.user_id, 0.0) + amount, 2)

                await websocket.send_text(json.dumps({
                    "event": "BET_CONFIRMED",
                    "round_id": room.round_id,
                    "bet_amount": room.round_bets[player.user_id],
                    "new_balance": player.balance
                }))

    except WebSocketDisconnect:
        if websocket in room.players:
            del room.players[websocket]
    except Exception as e:
        if websocket in room.players:
            del room.players[websocket]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rgs_server:app", host="0.0.0.0", port=8001, reload=False)
