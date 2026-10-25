---
name: ice-fishing-platform
description: Manage, start, inspect, and test the multi-tier Ice Fishing casino platform (Client Lobby, FastAPI Platform Core, Ledger DB, and RGS) with zero friction.
---

# Ice Fishing Platform Operations Skill

This skill guides running, inspecting, and presenting the playable Ice Fishing platform replica located in `platform/`.

## Frictionless Quick Start for Non-Technical Users

To launch the full stack with zero manual configuration or coding needed:
```bat
.\platform\run_platform.bat
```
This automatically boots:
- **Client Web Lobby**: `http://localhost:3000`
- **Platform Core Server**: `http://localhost:8000`
- **RGS Game Engine**: `http://localhost:8001`

Then simply open `http://localhost:3000` in Google Chrome or any modern browser.

## Component Overview

- **Web Lobby (`platform/client`)**: Static frontend hosted on HTTP port `3000`. Pure zero-dependency HTML5/JS.
- **Platform Core API (`platform/server/main.py`)**: FastAPI application on port `8000`. Handles user auth, session tokens, wallet balances, debit/credit transactions, and game launching.
- **Double-Entry Ledger (`platform/server/ledger.py` & `platform_core.db`)**: SQLite-backed ACID compliant financial ledger ensuring zero balance drifting.
- **RGS (`platform/rgs/rgs_server.py`)**: Remote Gaming Server on port `8001`. Resolves spins, validates bets, and coordinates with platform ledger.

## Manual Commands (If Individual Process Control is Desired)
```powershell
# Platform API
cd platform/server
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Game RGS
cd platform/rgs
python -m uvicorn rgs_server:app --host 0.0.0.0 --port 8001

# Web Client
cd platform/client
python -m http.server 3000 --bind 0.0.0.0
```

## Testing & Verifying Health
- Platform API Health / Docs: `GET http://localhost:8000/docs`
- RGS Health / Docs: `GET http://localhost:8001/docs`
- Web Lobby: `http://localhost:3000`
