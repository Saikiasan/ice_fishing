---
name: ice-fishing-telemetry
description: Listen to, simulate, and analyze Ice Fishing game events, WebSocket packet flows, and spin history datasets.
---

# Ice Fishing Game Telemetry & Data Analysis Skill

This skill provides reference information and tool patterns for inspecting real-time WebSocket gameplay events and historical spin simulation data for the Ice Fishing game replica (`IceFishing000001`).

## Gameplay WebSocket Details

- **Protocol Format**: Standard JSON payload containing `type` and `args` fields.
- **Round Sequence**:
  - `icefishing.betsOpen`: Sent at round start. Contains `gameId`, `gameNumber`, `timeRemaining`, and `spinInfo` (`sector`, `speed`, `direction`).
  - `icefishing.betsClosed`: Wagers locked.
  - `icefishing.wheelSpinning`: Contains `leafWheelMultipliers` mappings.
  - `icefishing.gameResult`: Winning sector index, resulting fish bonus multiplier, or leaf multiplier.

## Available Simulation & Analytics Scripts

- [direct_listener.py](file:///d:/Codes/ice_fishing/direct_listener.py): Real-time WebSocket listener that attaches to game server streams.
- [analyze_history.py](file:///d:/Codes/ice_fishing/analyze_history.py): Analyzes recorded spin rounds and calculates sector frequencies.
- [analyze_todays_spins.py](file:///d:/Codes/ice_fishing/analyze_todays_spins.py): Daily breakdown of game payouts and RTP statistics.
- [export_exact_spins.py](file:///d:/Codes/ice_fishing/export_exact_spins.py): Exports recorded spin sessions into clean CSV/JSON datasets.

## Analyzing Spin Datasets
Run the analysis script directly via Python:
```powershell
python analyze_history.py
```
Outputs statistical distributions, fish bonus frequencies, and leaf outcomes across captured round histories.
