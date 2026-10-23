# 🎣 Evolution Ice Fishing: Reverse Engineering, Analytics & Predictor HUD

A comprehensive technical documentation detailing the protocol reverse engineering, real-time WebSocket telemetry, statistical mechanics, and in-game HUD developed for Evolution's **"Ice Fishing"** live casino money-wheel game (`IceFishing000001`).

---

## 📋 Table of Contents
1. [Architecture & System Overview](#1-architecture--system-overview)
2. [Wheel Geometry & Mathematical Model](#2-wheel-geometry--mathematical-model)
3. [WebSocket Protocol Reverse Engineering](#3-websocket-protocol-reverse-engineering)
4. [Real-Time Advance Latency (The 4-Second Window)](#4-real-time-advance-latency-the-4-second-window)
5. [Predictability & Physics Analysis](#5-predictability--physics-analysis)
6. [Tools & Deliverables](#6-tools--deliverables)
   - [Tampermonkey In-Game Terminal HUD](#a-tampermonkey-in-game-terminal-hud)
   - [Python Real-Time Telemetry Engine](#b-python-real-time-telemetry-engine)
   - [Datasets & Exporters](#c-datasets--exporters)
7. [Installation & Usage Guide](#7-installation--usage-guide)

---

## 1. Architecture & System Overview

The system captures, analyzes, and visualizes live wheel telemetry using two parallel architectures:

```
[ Evolution Game Servers ]
           │
           │  (WSS Encrypted Stream)
           ▼
[ Chrome Browser (Ice Fishing Tab) ]
   ├── [ Vanilla Game Engine ] (Renders WebGL & Video feed)
   └── [ Tampermonkey Stealth Proxy ]
           ├── [ Floating Terminal HUD ] (Directly overlays live advice & early results)
           └── (Optional Local Relay: ws://127.0.0.1:8765)
                   ▼
           [ Python Real-Time Engine (live_engine.py) ]
                   ├── Spin Physics / Displacement Tracker
                   ├── Virtual Bankroll Strategy Simulator
                   └── Dataset Persistence (ice_fishing_dataset.json)
```

---

## 2. Wheel Geometry & Mathematical Model

The Ice Fishing money wheel is comprised of **53 physical sectors** (numbered 0 to 52). 

### Empirical vs. Theoretical Distribution (Benchmarked over 81 live rounds)

| Internal Key | Display Name | Role | Sector Count | Theoretical Prob. | Empirical Prob. (81 Spins) | Base Payout |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `Leaf1` | **Light Leaf (L1)** | Base Safe | ~24 | 45.3% | **50.6%** | 1:1 (or up to 10x) |
| `Leaf2` | **Dark Leaf (L2)** | Base Safe | ~22 | 41.5% | **32.1%** | 1:1 (or up to 10x) |
| `LilBlues` | **Lil' Blues** | Fish Bonus | 4 | 7.5% | **6.2%** | Bonus (up to 100x+) |
| `BigOranges` | **Big Oranges** | Fish Bonus | 2 | 3.8% | **7.4%** | Bonus (up to 500x+) |
| `HugeReds` | **Huge Reds** | Jackpot Fish | 1 | 1.9% | **3.7%** | Bonus (up to 10,000x) |
| **Total** | | | **53** | **100.0%** | **100.0%** | |

> **Key Statistical Rule:**  
> **Leaves account for ~86.8% of the wheel.** Fish bonus rounds land only ~13.2% of the time (approx. 1 in every 7 to 8 spins).

---

## 3. WebSocket Protocol Reverse Engineering

The game connects to the following endpoint:
```text
wss://ezugi.evo-games.com/public/icefishing/player/game/IceFishing000001/socket?messageFormat=json&EVOSESSIONID=...
```

### Event Lifecycle per Round

1. **`icefishing.betsOpen` (T = 0s)**  
   Betting window opens (~7 seconds). Transmits starting position and rotation direction:
   ```json
   {
     "type": "icefishing.betsOpen",
     "args": {
       "gameId": "18dec54ddcd2fdcad6a46da8",
       "gameNumber": "17:50:39",
       "timeRemaining": 6934,
       "spinInfo": {
         "sector": 41,
         "speed": "Medium",
         "direction": "Clockwise"
       }
     }
   }
   ```

2. **`icefishing.betsClosed` (T = 7s)**  
   Server locks all bets. No further chips are accepted.

3. **`icefishing.wheelSpinning` (T = 10.5s)**  
   Server designates random multipliers onto specific physical wheel sectors:
   ```json
   {
     "type": "icefishing.wheelSpinning",
     "args": {
       "leafWheelMultipliers": {
         "11": { "result": "Leaf1", "multiplier": { "value": 4, "level": "Low" } },
         "28": { "result": "Leaf2", "multiplier": { "value": 5, "level": "Low" } }
       }
     }
   }
   ```

4. **`icefishing.wheelStopping` (T = 14s)**  
   Server declares the confirmed winning sector **4 seconds before visual landing**:
   ```json
   {
     "type": "icefishing.wheelStopping",
     "args": {
       "sector": 39,
       "timeRemaining": 4000
     }
   }
   ```

5. **`icefishing.spinHistory` (Post-Round)**  
   Server broadcasts the updated 73-spin sliding historical ledger.

---

## 4. Real-Time Advance Latency (The 4-Second Window)

Because video encoding, WebRTC packet buffering, and physical wheel friction take time to render on client screens, Evolution broadcasts `icefishing.wheelStopping` as soon as the optical flapper sensors lock the physical stop.

* **Client Video Display:** The wheel takes an additional **4,000 milliseconds** (`wheel_slow_down_duration`) to visually come to rest.
* **Our HUD Advantage:** The HUD parses the incoming packet instantly and displays `>>> SECTOR X! <<<` in glowing neon green **4 seconds ahead** of the video broadcast.

---

## 5. Predictability & Physics Analysis

We analyzed consecutive spins in [`ice_fishing_dataset.json`](file:///d:/Codes/ice_fishing/ice_fishing_dataset.json) to measure modular displacement ($\Delta = \text{Landed} - \text{Start} \pmod{54}$):

* **Clockwise Spins ($\Delta$):** `[28, 1, 52, 31, 45, 31, 47, 38, 41, 43, 27]`  
  - Mean: **34.9 sectors** | Standard Deviation: **$\pm 14.8$**
* **Counter-Clockwise Spins ($\Delta$):** `[45, 35, 42, 22, 52, 12, 20, 10, 26, 35]`  
  - Mean: **29.9 sectors** | Standard Deviation: **$\pm 13.9$**

### The Technical Conclusion on Prediction:
1. **No Dealer "Signature":** The variance spans almost the entire wheel circumference (1 to 52 sectors). Physical pin resistance and variable motor force eliminate deterministic mechanical prediction.
2. **Timing Barrier:** `betsClosed` executes at $T=0$, whereas multipliers and physical deceleration occur at $T \ge 3.5s$.
3. **Statistically Sound Play:** The optimal strategy is not chasing single numbers, but:
   - Maintaining primary coverage on **Light Leaf** and **Dark Leaf** (~83% cumulative hit frequency).
   - Using the **Drought Tracker** to avoid burning bankroll on rare fish during prolonged dry spells ($>40$ rounds).

---

## 6. Tools & Deliverables

### A. Tampermonkey In-Game Terminal HUD (`tampermonkey_hud.js`)
* **Design:** High-contrast pitch-black and neon-green (`#00ff66`) terminal theme.
* **Live Probability Matrix:** Displays exact real-time percentages for all 5 outcomes.
* **Next Round Predictor (Top 3 Picks):** Ranks the top 3 optimal selections before betting closes.
* **Drought Tracker:** Displays rounds elapsed since `Huge Reds`, `Big Oranges`, and `Lil' Blues` last landed.
* **Advance Alert:** Flashes winning sector 4 seconds early.

### B. Python Real-Time Engine (`live_engine.py`)
* WebSocket server on `ws://127.0.0.1:8765`.
* Calculates rolling displacement deltas for clockwise/counterclockwise spins.
* Runs a live **Virtual Bankroll Strategy Simulator** (₹1,000 credit) tracking real-time P&L and drawdowns.
* Automatically writes completed rounds to persistent JSON storage.

### C. Datasets & Exporters
* [`exact_gameplay_history.csv`](file:///d:/Codes/ice_fishing/exact_gameplay_history.csv): 81 verified rounds with exact spin index, multipliers, and display names.
* [`ice_fishing_dataset.json`](file:///d:/Codes/ice_fishing/ice_fishing_dataset.json): Raw round data including start sector, direction, and winning sector.
* [`export_exact_spins.py`](file:///d:/Codes/ice_fishing/export_exact_spins.py): Python utility to export game history to CSV.

---

## 7. Installation & Usage Guide

### Running the Terminal In-Game HUD:
1. Install the [Tampermonkey](https://www.tampermonkey.net/) extension in Chrome.
2. Create a new user script.
3. Paste the contents of [`tampermonkey_hud.js`](file:///d:/Codes/ice_fishing/tampermonkey_hud.js).
4. Save with `Ctrl + S` and refresh the Ice Fishing game tab.

### Running the Python Live Engine (Optional):
1. In PowerShell:
   ```powershell
   cd d:\Codes\ice_fishing
   python live_engine.py
   ```
2. The engine will listen on `ws://127.0.0.1:8765` and log live stats and strategy P&L.

---

## 8. Author & License

Developed and maintained by **Ankit Saikia**.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

