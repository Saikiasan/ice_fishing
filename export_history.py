import json
import csv
import os

JSON_FILE = "ice_fishing_dataset.json"
CSV_FILE = "ice_fishing_history.csv"

if not os.path.exists(JSON_FILE):
    print("No dataset file found yet.")
    exit()

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} recorded rounds.")

# Write to CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Game ID", "Game Number", "Timestamp", "Start Sector", "Direction", "Winning Sector", "Displacement"])
    
    for gid, r in data.items():
        writer.writerow([
            gid,
            r.get("gameNumber", ""),
            r.get("timestamp", ""),
            r.get("startSector", ""),
            r.get("direction", ""),
            r.get("winningSector", ""),
            r.get("displacement", "")
        ])

print(f"[SUCCESS] Exported all rounds to: {CSV_FILE}")
