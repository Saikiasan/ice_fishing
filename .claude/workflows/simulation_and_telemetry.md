# Game Simulation & Telemetry Workflow

This workflow guides Claude and operators through running game simulations, spinning round analytics, and statistical benchmarking.

---

## Step 1: Run Standalone WebSocket Game Server
To simulate live WebSocket game broadcast rounds independently:
```powershell
python evo_backend_server.py
```
This serves simulated live game rounds, multiplier distributions, and wheel physics locally.

---

## Step 2: Run Telemetry Listener
To monitor real-time JSON packets broadcast by the game server:
```powershell
python direct_listener.py
```
Expected output: Streams incoming `betsOpen`, `wheelSpinning`, and `gameResult` payloads.

---

## Step 3: Run Statistical Analytics
To benchmark sector probability and return models over captured round history:
```powershell
# Analyze overall sector frequencies
python analyze_history.py

# Analyze daily session summaries & RTP
python analyze_todays_spins.py
```

---

## Step 4: Export Clean Datasets
To extract clean CSV/JSON spin session history:
```powershell
python export_exact_spins.py
```
Result files generated:
- `exact_gameplay_history.csv`
- `exact_gameplay_history.json`
