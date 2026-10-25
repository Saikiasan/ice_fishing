# CLAUDE.md - Ice Fishing Money-Wheel Game Platform Guide

## Project Nature & Mission
This project is an **interactive web-based educational replica and standalone implementation** of the popular **"Ice Fishing"** 53-sector money-wheel live casino game. 

It provides:
1. A complete local gaming server and client platform.
2. Real-time game state simulation, probability modeling, and RNG spin mechanics.
3. Live telemetry analysis and historical simulation tools.
4. Production-ready financial ledger and gaming platform architecture documentation.

---

## ⚡ Zero-Friction Handover / Quick Start

For any user or assistant staging this repository with no prior code setup, everything can be run with **zero code modifications**:

### One-Click Launch (Recommended)
Simply run the startup batch file from the root or platform directory:
```bat
.\platform\run_platform.bat
```
This automatically launches all necessary background processes in separate windows:
- **Platform Core & Wallet API**: `http://localhost:8000` (FastAPI backend + SQLite ledger)
- **RGS Game Server**: `http://localhost:8001` (Game mechanics & spin engine)
- **Web Lobby & Client**: `http://localhost:3000` (Playable game interface)

Open your web browser at: **`http://localhost:3000`**

---

## Architecture & Subsystems

1. **Integrated Platform Suite (`/platform`)**
   - **Player Lobby (`platform/client/index.html`)**: Clean, dependency-free HTML5/ES6 frontend served on port `3000`.
   - **Platform Core Server (`platform/server/main.py`)**: FastAPI backend on port `8000` managing accounts, authentication tokens, balance tracking, and game launch sessions.
   - **Double-Entry Financial Ledger (`platform/server/ledger.py`)**: SQLite-backed database (`platform_core.db`) enforcing strict double-entry accounting with zero rounding drift.
   - **Remote Gaming Server (RGS) (`platform/rgs/rgs_server.py`)**: Standalone game engine running on port `8001`. Handles 53-sector wheel RNG, bonus multiplier triggers, bet validation, and payout settlement.

2. **Standalone Mock Game Server (`evo_backend_server.py` & `/evo_server`)**
   - Self-contained WebSocket game server simulating real-time game rounds, multiplier assignments, and physics for testing.
   - To launch:
     ```powershell
     python evo_backend_server.py
     ```

3. **Game Mechanics, Analytics & Simulation Tools**
   - **`analyze_history.py`**: Calculates empirical sector distributions and payout frequencies.
   - **`analyze_todays_spins.py`**: Daily summary of spins, RTP benchmarking, and bonus round intervals.
   - **`export_exact_spins.py`**: Exports recorded spin sessions into clean CSV and JSON datasets.
   - **`direct_listener.py`**: WebSocket stream receiver and inspector for local or network game server instances.

4. **Production Architecture & Financial Application Docs (`/financial application solution development and startup phase`)**
   - Master technical solutions covering payment gateway integration, treasury management, risk & anomaly detection, and operational KPIs.

---

## Wheel Mathematics & Payout Model

The game is centered on a precision **53-sector wheel** (indexed 0 to 52):

| Sector Type | Symbol Key | Sector Count | Probability | Base Payout / Action |
| :--- | :--- | :---: | :---: | :--- |
| **Light Leaf (L1)** | `Leaf1` | ~24 | 45.3% | 1:1 base payout (up to 10x with random multiplier) |
| **Dark Leaf (L2)** | `Leaf2` | ~22 | 41.5% | 1:1 base payout (up to 10x with random multiplier) |
| **Lil' Blues** | `LilBlues` | 4 | 7.5% | Interactive fish bonus mini-game |
| **Big Oranges** | `BigOranges` | 2 | 3.8% | High multiplier fish bonus mini-game |
| **Huge Reds** | `HugeReds` | 1 | 1.9% | Super jackpot fish mini-game (up to 10,000x) |
| **Total** | | **53** | **100.0%** | |

**Distribution Rule**: Safe leaf sectors represent **~86.8%** of the wheel. Fish bonus rounds occur on average once every **7 to 8 spins** (~13.2%).

---

## Round Lifecycle & State Flow

Every spin follows a 4-phase sequence:
1. **`betsOpen`**: Betting window opens (~7 seconds). Transmits starting wheel sector and rotation direction.
2. **`betsClosed`**: Wagering closes. Player bets are locked and validated against ledger balances.
3. **`wheelSpinning`**: Wheel rotates; server assigns dynamic random multipliers onto specific leaf or bonus sectors.
4. **`gameResult` / Settlement**: Wheel settles on the winning sector; multiplier is calculated; winning credits are posted to player wallets.

---

## Coding & Operational Guidelines for Claude

- **Zero-Modification Policy**: Do not modify existing working scripts or core server files unless explicitly requested by the user.
- **Simplicity First**: When explaining or demonstrating the project to non-technical users, always favor running `.\platform\run_platform.bat` or single-step Python scripts.
- **Port Invariants**:
  - Web Lobby: `3000`
  - Platform Core API: `8000`
  - RGS Game Server: `8001`
- **Financial Precision**: All monetary calculations in `ledger.py` use integer/cents representation to ensure strict precision.
