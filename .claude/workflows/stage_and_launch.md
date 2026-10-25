# Stage & Launch Platform Workflow

This workflow provides Claude and any user with a foolproof, frictionless procedure to stage, boot, and verify the entire Ice Fishing gaming suite.

## Pre-conditions
- Windows OS with Python 3.10+ installed.
- Repository cloned locally.

---

## Step 1: One-Click Startup
Execute the root platform launcher:
```bat
.\platform\run_platform.bat
```
*Note: This command spawns three dedicated CMD windows:*
1. **Platform Core API** (`http://localhost:8000`)
2. **RGS Game Server** (`http://localhost:8001`)
3. **Player Web Lobby** (`http://localhost:3000`)

---

## Step 2: Health Verification
Confirm all microservices respond correctly:
1. **Platform API Health Check:**
   - URL: `http://localhost:8000/docs` (FastAPI Swagger documentation)
2. **RGS Server Health Check:**
   - URL: `http://localhost:8001/docs` (Swagger documentation)
3. **Player Web Client:**
   - URL: `http://localhost:3000`

---

## Step 3: Interactive Verification
1. Open `http://localhost:3000` in Google Chrome or any modern browser.
2. Observe user wallet balance initialized from SQLite ledger (`platform_core.db`).
3. Place a test chip bet on Leaf or Fish bonus positions during the betting countdown.
4. Verify spin outcome and credit settlement post-round.

---

## Troubleshooting & Zero-Break Invariant
- **Port Conflicts**: Ensure ports 3000, 8000, and 8001 are not occupied.
- **Strict Invariant**: Do not modify `platform/server/ledger.py` or database models during execution.
