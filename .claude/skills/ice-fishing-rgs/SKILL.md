---
name: ice-fishing-rgs
description: Understand, simulate, and configure the Ice Fishing Remote Gaming Server (RGS), 53-sector wheel RNG, multiplier allocations, and payout mechanics.
---

# Ice Fishing Game Engine & RGS Skill

This skill explains and guides the game logic, RNG outcome generation, and payout rules for the Ice Fishing money-wheel game replica (`IceFishing000001`).

## 53-Sector Wheel Layout

The physical wheel contains 53 indexed positions (0 to 52):

| Symbol Key | Display Name | Sectors | Probability | Base Payout |
| :--- | :--- | :---: | :---: | :--- |
| `Leaf1` | Light Leaf (L1) | ~24 | 45.3% | 1:1 (or up to 10x) |
| `Leaf2` | Dark Leaf (L2) | ~22 | 41.5% | 1:1 (or up to 10x) |
| `LilBlues` | Lil' Blues | 4 | 7.5% | Bonus multiplier game |
| `BigOranges` | Big Oranges | 2 | 3.8% | High bonus game |
| `HugeReds` | Huge Reds | 1 | 1.9% | Jackpot (up to 10,000x) |

## Round Lifecycle & State Machine

1. **`betsOpen`**:
   - Starting sector emitted.
   - Betting countdown active (~7 seconds).
2. **`betsClosed`**:
   - Wagering locked.
   - Total bets tallied and validated against player balance.
3. **`wheelSpinning`**:
   - Multipliers distributed dynamically across random leaf or bonus sectors.
4. **`gameResult` / Settlement**:
   - Final winning sector determined by RNG.
   - Multipliers applied.
   - Payout transactions sent to double-entry ledger.

## RGS Server Locations
- Interactive RGS Server: [rgs_server.py](file:///d:/Codes/ice_fishing/platform/rgs/rgs_server.py)
- Standalone Mock Server: [evo_backend_server.py](file:///d:/Codes/ice_fishing/evo_backend_server.py)
