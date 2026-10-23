import sys
import asyncio
import json
import os
import websockets
from datetime import datetime

# Windows console encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILE = "live_stream_records.jsonl"

async def handler(websocket):
    print("\n🟢 [CONNECTED] Chrome game stream connected to Python!", flush=True)
    active_multipliers = {}

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except Exception:
                continue

            msg_type = data.get("type", "")
            args = data.get("args", {})

            # 1. Round Start
            if msg_type == "icefishing.betsOpen":
                active_multipliers = {}
                game_num = args.get("gameNumber", "")
                spin_info = args.get("spinInfo", {})
                print(f"\n🎲 [BETS OPEN #{game_num}] Start Sector: {spin_info.get('sector')} | Direction: {spin_info.get('direction')}", flush=True)

            # 2. Multipliers Announced
            elif msg_type == "icefishing.wheelSpinning":
                mults = args.get("leafWheelMultipliers", {})
                active_multipliers = mults
                if mults:
                    items = [f"Sector {s}: {m['multiplier']['value']}x ({m['result']})" for s, m in mults.items()]
                    print(f"⚡ [MULTIPLIERS ACTIVE ({len(items)})]: {', '.join(items)}", flush=True)

            # 3. Winning Sector (4s Advance Signal)
            elif msg_type == "icefishing.wheelStopping":
                sector = args.get("sector")
                game_id = args.get("gameId")
                game_num = args.get("gameNumber")
                
                # Check if landed sector won a multiplier
                won_mult = 1
                if str(sector) in active_multipliers:
                    won_mult = active_multipliers[str(sector)].get("multiplier", {}).get("value", 1)

                print(f"🚨 [EARLY RESULT (4s AHEAD)] Sector: {sector} | Multiplier Won: {won_mult}x!", flush=True)

                # Append raw record to JSON Lines file
                record = {
                    "gameId": game_id,
                    "gameNumber": game_num,
                    "winningSector": sector,
                    "multiplier": won_mult,
                    "timestamp": datetime.now().isoformat()
                }
                with open(DATA_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")

            # 4. Spin History Window
            elif msg_type == "icefishing.spinHistory":
                results = args.get("results", [])
                latest = results[0] if results else {}
                mult_info = latest.get("wheelMultiplier", {}).get("value", 1)
                print(f"📋 [HISTORY UPDATE] Latest Confirmed: {latest.get('result')} ({mult_info}x)", flush=True)

    except websockets.exceptions.ConnectionClosed:
        print("🔴 [DISCONNECTED] Chrome stream disconnected.", flush=True)

async def main():
    print("🚀 Ice Fishing Python Real-Time Stream Listener running on ws://127.0.0.1:8765...", flush=True)
    async with websockets.serve(handler, "127.0.0.1", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nListener stopped gracefully.", flush=True)
