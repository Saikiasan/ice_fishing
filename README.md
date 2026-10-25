# 🎣 Ice Fishing: Interactive Money-Wheel Game Platform & Simulation Engine

A comprehensive web platform, game server implementation, and statistical simulation engine reproducing the popular **53-sector "Ice Fishing" money-wheel game** (`IceFishing000001`).

---

## 📋 Table of Contents
1. [Project Overview](#1-project-overview)
2. [⚡ Frictionless Quick Start](#2-frictionless-quick-start)
3. [Architecture & Components](#3-architecture--components)
4. [Wheel Geometry & Mathematical Model](#4-wheel-geometry--mathematical-model)
5. [Round Lifecycle & State Machine](#5-round-lifecycle--state-machine)
6. [Simulation & Analytics Tools](#6-simulation--analytics-tools)
7. [Enterprise Ledger & Platform Architecture](#7-enterprise-ledger--platform-architecture)
8. [License](#8-license)

---

## 1. Project Overview

This repository provides a complete, self-contained educational implementation and testbench of a live money-wheel casino game. It includes:
- **Full-Stack Playable Platform**: Modern web lobby, user authentication, double-entry financial ledger, and Remote Gaming Server (RGS).
- **Standalone Game Simulation Server**: High-fidelity WebSocket server simulating real-time game rounds, dynamic multiplier assignments, and spin physics.
- **Statistical Analytics & Datasets**: Benchmarking tools analyzing sector hit rates, volatility, and player return-to-player (RTP) models.
- **Zero-Friction Staging**: Turnkey launch scripts ensuring instant local operation with zero configuration needed.

---

## 2. ⚡ Frictionless Quick Start

To launch the complete platform locally with a single command:

```bat
.\platform\run_platform.bat
```

This automatically starts all 3 core services in their own terminal windows:
- **Web Lobby & Client**: `http://localhost:3000`
- **Platform Core & Wallet API**: `http://localhost:8000` (FastAPI backend + SQLite ledger)
- **RGS Game Engine**: `http://localhost:8001` (Game mechanics & spin resolution)

Once started, simply open **`http://localhost:3000`** in your browser.

---

## 3. Architecture & Components

```
                    ┌─────────────────────────┐
                    │       Web Browser       │
                    │   http://localhost:3000 │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
      ┌─────────────────────┐         ┌─────────────────────┐
      │  Platform Core API  │         │   RGS Game Server   │
      │   (FastAPI :8000)   │◄───────►│   (FastAPI :8001)   │
      └──────────┬──────────┘         └─────────────────────┘
                 │
                 ▼
      ┌─────────────────────┐
      │ Double-Entry Ledger │
      │ (platform_core.db)  │
      └─────────────────────┘
```

### Core Subsystems:
1. **Player Web Lobby (`platform/client`)**: Clean HTML5/ES6 client interface with real-time balance updates, chip placement, and game launching.
2. **Platform Server (`platform/server/main.py`)**: Manages player accounts, secure session tokens, wallet balances, and game launch orchestration.
3. **Double-Entry Financial Ledger (`platform/server/ledger.py`)**: ACID-compliant SQLite ledger ensuring zero balance drifting or floating-point discrepancies.
4. **Remote Gaming Server (RGS) (`platform/rgs/rgs_server.py`)**: Manages the 53-sector wheel RNG, bonus multiplier distributions, and round settlement.
5. **Standalone Simulation Server (`evo_backend_server.py`)**: Independent WebSocket game server emulating real-time wheel spins and event streaming for testing.

---

## 4. Wheel Geometry & Mathematical Model

The Ice Fishing money wheel is comprised of **53 physical sectors** (numbered 0 to 52):

| Symbol Key | Display Name | Role | Sector Count | Probability | Base Payout |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `Leaf1` | **Light Leaf (L1)** | Base Safe | ~24 | **45.3%** | 1:1 (or up to 10x with multiplier) |
| `Leaf2` | **Dark Leaf (L2)** | Base Safe | ~22 | **41.5%** | 1:1 (or up to 10x with multiplier) |
| `LilBlues` | **Lil' Blues** | Fish Bonus | 4 | **7.5%** | Interactive mini-game (up to 100x+) |
| `BigOranges` | **Big Oranges** | Fish Bonus | 2 | **3.8%** | High mini-game (up to 500x+) |
| `HugeReds` | **Huge Reds** | Jackpot Fish | 1 | **1.9%** | Super bonus game (up to 10,000x) |
| **Total** | | | **53** | **100.0%** | |

> **Key Game Mechanics:**
> - Safe Leaf sectors cover **86.8%** of the wheel, providing steady, lower-volatility outcomes.
> - Fish bonus mini-games occur on average once every **7 to 8 spins** (~13.2%).

---

## 5. Round Lifecycle & State Machine

Each spin round progresses through standard lifecycle events:

1. **`betsOpen` (T = 0s)**: Betting window opens (~7 seconds). Transmits starting wheel sector and rotation direction.
2. **`betsClosed` (T = 7s)**: Wagering locks. Player wagers are validated against ledger balances.
3. **`wheelSpinning` (T = 10.5s)**: Multipliers are assigned dynamically across random leaf or bonus sectors.
4. **`gameResult` / Settlement (T = 15s)**: Wheel settles on the winning sector; multiplier is calculated; winning credits are posted to player wallets.

---

## 6. Simulation & Analytics Tools

The repository includes utilities to inspect game data, test bankroll strategies, and verify RNG fairness:

- **`analyze_history.py`**: Computes empirical hit rates and variance over captured rounds.
- **`analyze_todays_spins.py`**: Generates daily RTP benchmarks and bonus round occurrence intervals.
- **`export_exact_spins.py`**: Formats and exports historical round records to clean CSV/JSON formats.
- **`direct_listener.py`**: Real-time WebSocket listener to observe and log live round event streams.

---

## 7. Enterprise Ledger & Platform Architecture

Detailed architectural specifications and production-ready designs are documented in:
- [`00_master_solution_plan.md`](file:///d:/Codes/ice_fishing/financial%20application%20solution%20development%20and%20startup%20phase/00_master_solution_plan.md)
- [`01_system_architecture_and_data_flow.md`](file:///d:/Codes/ice_fishing/financial%20application%20solution%20development%20and%20startup%20phase/01_system_architecture_and_data_flow.md)
- [`02_executive_dashboard_and_realtime_kpis.md`](file:///d:/Codes/ice_fishing/financial%20application%20solution%20development%20and%20startup%20phase/02_executive_dashboard_and_realtime_kpis.md)
- [`03_payments_gateway_settlement_and_treasury.md`](file:///d:/Codes/ice_fishing/financial%20application%20solution%20development%20and%20startup%20phase/03_payments_gateway_settlement_and_treasury.md)
- [`04_risk_fraud_and_anomaly_detection.md`](file:///d:/Codes/ice_fishing/financial%20application%20solution%20development%20and%20startup%20phase/04_risk_fraud_and_anomaly_detection.md)

---

## 8. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
