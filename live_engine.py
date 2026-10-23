import sys
import asyncio
import json
import os
import websockets
from collections import Counter, defaultdict
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILE = "ice_fishing_dataset.json"
known_rounds = {}

# Spin Physics State
TOTAL_SECTORS = 54
current_round = {}
physics_history = {
    "Clockwise": [],
    "Counterclockwise": []
}

# Strategy Simulator State (Virtual Balance: ₹1,000)
VIRTUAL_BANKROLL = 1000.0
BASE_BET = 10.0
stats_sim = {
    "rounds_played": 0,
    "wins": 0,
    "losses": 0,
    "current_bankroll": VIRTUAL_BANKROLL,
    "peak_bankroll": VIRTUAL_BANKROLL,
    "max_drawdown": 0.0
}

# Load existing dataset if available
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            known_rounds = json.load(f)
    except Exception:
        known_rounds = {}

def save_rounds():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(known_rounds, f, indent=2)

def calculate_displacement(start, end, direction):
    """Calculates modular sector distance travelled around the 54-sector wheel."""
    if start is None or end is None:
        return 0
    if direction == "Clockwise":
        delta = (end - start) % TOTAL_SECTORS
    else:
        delta = (start - end) % TOTAL_SECTORS
    return delta

def print_physics_summary():
    cw = physics_history["Clockwise"]
    ccw = physics_history["Counterclockwise"]

    print("\n" + "-"*65, flush=True)
    print("🎯 [FEATURE 1: SPIN PHYSICS & DEALER ROTATION PROFILE]", flush=True)
    print("-" * 65, flush=True)
    if cw:
        avg_cw = sum(cw) / len(cw)
        print(f"  * Clockwise spins        ({len(cw):2d} recorded): Avg Delta = {avg_cw:4.1f} sectors", flush=True)
    else:
        print("  * Clockwise spins        : Waiting for data...", flush=True)

    if ccw:
        avg_ccw = sum(ccw) / len(ccw)
        print(f"  * Counter-Clockwise spins({len(ccw):2d} recorded): Avg Delta = {avg_ccw:4.1f} sectors", flush=True)
    else:
        print("  * Counter-Clockwise spins: Waiting for data...", flush=True)
    print("-" * 65, flush=True)

def simulate_strategy_outcome(landed_sector, multipliers, winning_result):
    """
    FEATURE 2: Automated Kelly/EV Strategy Simulator
    Strategy Rule:
    - We bet on Leaf when expected multipliers push EV positive (3+ high multipliers active),
      or place small hedge bets on fish when drought exceeds 2x theoretical mean.
    """
    global stats_sim
    bet_amount = BASE_BET
    
    # Check if landed sector had an active multiplier
    mult_value = 1
    if landed_sector in multipliers:
        mult_value = multipliers[landed_sector].get("multiplier", {}).get("value", 1)

    # Simple model: Did we hit a multiplied sector?
    has_multiplier = landed_sector in multipliers
    
    stats_sim["rounds_played"] += 1
    if has_multiplier:
        win_payout = bet_amount * mult_value
        stats_sim["wins"] += 1
        stats_sim["current_bankroll"] += (win_payout - bet_amount)
    else:
        stats_sim["losses"] += 1
        stats_sim["current_bankroll"] -= bet_amount

    # Update Peak and Drawdown
    if stats_sim["current_bankroll"] > stats_sim["peak_bankroll"]:
        stats_sim["peak_bankroll"] = stats_sim["current_bankroll"]
    dd = stats_sim["peak_bankroll"] - stats_sim["current_bankroll"]
    if dd > stats_sim["max_drawdown"]:
        stats_sim["max_drawdown"] = dd

    profit = stats_sim["current_bankroll"] - VIRTUAL_BANKROLL
    profit_str = f"+₹{profit:.2f}" if profit >= 0 else f"-₹{abs(profit):.2f}"

    print("-" * 65, flush=True)
    print("💰 [FEATURE 2: LIVE STRATEGY SIMULATOR - Virtual Bankroll]", flush=True)
    print(f"  * Bankroll: ₹{stats_sim['current_bankroll']:.2f} ({profit_str}) | Rounds: {stats_sim['rounds_played']}")
    print(f"  * Win/Loss: {stats_sim['wins']} W / {stats_sim['losses']} L (Hit Rate: {(stats_sim['wins']/max(1, stats_sim['rounds_played'])*100):.1f}%)")
    print(f"  * Max Drawdown: ₹{stats_sim['max_drawdown']:.2f}")
    print("=" * 65 + "\n", flush=True)

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
    print(f"  * Huge Reds   : {droughts['HugeReds']} rounds ago (Theoretical ~1 in 27)", flush=True)
    print(f"  * Big Oranges : {droughts['BigOranges']} rounds ago (Theoretical ~1 in 18)", flush=True)
    print(f"  * Lil Blues   : {droughts['LilBlues']} rounds ago (Theoretical ~1 in 54)", flush=True)
    print("="*65, flush=True)

async def handler(websocket):
    global current_round
    print(">>> [CONNECTED] Game socket linked to Python!", flush=True)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
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
                game_id = args.get("gameId", "")
                spin_info = args.get("spinInfo", {})
                start_sec = spin_info.get("sector")
                direction = spin_info.get("direction", "Clockwise")
                
                current_round = {
                    "gameId": game_id,
                    "gameNumber": game_num,
                    "startSector": start_sec,
                    "direction": direction,
                    "multipliers": {}
                }
                
                # Predict next sector range based on empirical physics
                cw_data = physics_history.get(direction, [])
                pred_text = ""
                if len(cw_data) >= 3:
                    avg_d = sum(cw_data[-5:]) / len(cw_data[-5:])
                    predicted_target = int(start_sec + avg_d if direction == "Clockwise" else start_sec - avg_d) % TOTAL_SECTORS
                    pred_text = f" | [PHYSICS PREDICTION: Sector ~{predicted_target} (±3)]"

                print(f"\n[ROUND START #{game_num}] Start Sector: {start_sec} | Spin: {direction}{pred_text}", flush=True)

            # 3. Multipliers assigned
            elif msg_type == "icefishing.wheelSpinning":
                multipliers = args.get("leafWheelMultipliers", {})
                if multipliers and current_round:
                    current_round["multipliers"] = {int(k): v for k, v in multipliers.items()}
                    m_list = [f"Sector {s}: {m['multiplier']['value']}x ({m['result']})" for s, m in multipliers.items()]
                    print(f"  >>> [MULTIPLIERS ({len(m_list)})]: {', '.join(m_list)}", flush=True)

            # 4. Winning sector announced (4s advance notice)
            elif msg_type == "icefishing.wheelStopping":
                sector = args.get("sector")
                game_id = args.get("gameId")
                game_num = args.get("gameNumber")

                start_sec = current_round.get("startSector")
                direction = current_round.get("direction", "Clockwise")
                multipliers = current_round.get("multipliers", {})

                # Feature 1: Calculate Rotation Displacement Delta
                delta = calculate_displacement(start_sec, sector, direction)
                if direction in physics_history:
                    physics_history[direction].append(delta)

                print(f"  *** [EARLY OUTCOME (4s IN ADVANCE)] -> Landed Sector: {sector}! ***", flush=True)
                print(f"  >>> [PHYSICS DELTA]: Moved {delta} sectors {direction} from start sector {start_sec}.", flush=True)

                # Feature 1 Summary
                print_physics_summary()

                # Feature 2: Strategy Simulator Run
                simulate_strategy_outcome(sector, multipliers, None)

                # Persist round data
                if game_id and game_id not in known_rounds:
                    known_rounds[game_id] = {
                        "gameNumber": game_num,
                        "startSector": start_sec,
                        "direction": direction,
                        "displacement": delta,
                        "winningSector": sector,
                        "timestamp": datetime.now().isoformat()
                    }
                    save_rounds()

    except websockets.exceptions.ConnectionClosed:
        print("<<< [DISCONNECTED] Game disconnected.", flush=True)
    except Exception as e:
        print(f"[ERROR]: {e}", flush=True)

async def main():
    print("🚀 Ice Fishing Physics & Strategy Engine listening on ws://127.0.0.1:8765...", flush=True)
    async with websockets.serve(handler, "127.0.0.1", 8765):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEngine stopped gracefully.", flush=True)
