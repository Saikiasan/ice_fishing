import sys
import asyncio
import json
import os
import websockets
from collections import Counter
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILE = "ice_fishing_dataset.json"
known_rounds = {}

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            known_rounds = json.load(f)
            print(f"[STORAGE] Loaded {len(known_rounds)} existing rounds from {DATA_FILE}")
    except Exception:
        known_rounds = {}

def save_rounds():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(known_rounds, f, indent=2)

def print_stats(results):
    total = len(results)
    if total == 0:
        return
    counts = Counter(r.get("result") for r in results)
    
    droughts = {}
    for fish in ["HugeReds", "BigOranges", "LilBlues"]:
        drought = next((i for i, r in enumerate(reversed(results)) if r.get("result") == fish), total)
        droughts[fish] = drought

    print("\n" + "="*65, flush=True)
    print(f"[STATS] LIVE WINDOW ({total} spins analyzed) | {datetime.now().strftime('%H:%M:%S')}", flush=True)
    print("="*65, flush=True)
    for k, v in counts.most_common():
        pct = (v / total) * 100
        print(f"  {k:12}: {v:3d} spins ({pct:5.1f}%)", flush=True)
    
    print("-" * 65, flush=True)
    print("  [DROUGHT TRACKER] (Rounds since last appearance):", flush=True)
    print(f"  * Huge Reds   : {droughts['HugeReds']} rounds ago (Theoretical ~1 in 70)", flush=True)
    print(f"  * Big Oranges : {droughts['BigOranges']} rounds ago (Theoretical ~1 in 50)", flush=True)
    print(f"  * Lil Blues   : {droughts['LilBlues']} rounds ago (Theoretical ~1 in 18)", flush=True)
    print("="*65 + "\n", flush=True)

async def run_direct_client(ws_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://ezugi.evo-games.com"
    }

    print(f"Connecting directly to Evolution Game Server...", flush=True)
    async with websockets.connect(ws_url, additional_headers=headers) as ws:
        print("Connected directly! Streaming live game events in background...\n", flush=True)

        async for raw in ws:
            try:
                data = json.loads(raw)
            except Exception:
                continue

            msg_type = data.get("type", "")
            args = data.get("args", {})

            # 1. Historical ledger update
            if msg_type == "icefishing.spinHistory":
                results = args.get("results", [])
                print_stats(results)

            # 2. Round Start
            elif msg_type == "icefishing.betsOpen":
                game_num = args.get("gameNumber", "")
                spin_info = args.get("spinInfo", {})
                start_sec = spin_info.get("sector")
                direction = spin_info.get("direction")
                print(f"[ROUND START #{game_num}] Sector: {start_sec} | Spin: {direction}", flush=True)

            # 3. Multipliers assigned
            elif msg_type == "icefishing.wheelSpinning":
                multipliers = args.get("leafWheelMultipliers", {})
                if multipliers:
                    m_list = [f"Sector {s}: {m['multiplier']['value']}x ({m['result']})" for s, m in multipliers.items()]
                    print(f"  >>> [MULTIPLIERS]: {', '.join(m_list)}", flush=True)

            # 4. Winning sector announced (4s advance notice)
            elif msg_type == "icefishing.wheelStopping":
                sector = args.get("sector")
                game_id = args.get("gameId")
                game_num = args.get("gameNumber")
                print(f"  *** [EARLY OUTCOME (4s BEFORE SCREEN)] -> Landed Sector: {sector}! ***", flush=True)
                
                if game_id and game_id not in known_rounds:
                    known_rounds[game_id] = {
                        "gameNumber": game_num,
                        "winningSector": sector,
                        "timestamp": datetime.now().isoformat()
                    }
                    save_rounds()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        # Default to the active socket from your session
        target_url = "wss://ezugi.evo-games.com/public/icefishing/player/game/IceFishing000001/socket?messageFormat=json&EVOSESSIONID=uevqjt7fhdla6w35ufai3lzukm6bwcgrbd6dde09baa24437604cf4ffbf40b8f67116b50a976aea66&instance=0oak9e-uevqjt7fhdla6w35-IceFishing000001&client_version=6.20261014.73630.66407-7cee8b959e-r3"

    try:
        asyncio.run(run_direct_client(target_url))
    except KeyboardInterrupt:
        print("\nDirect client stopped.", flush=True)
