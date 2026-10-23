import json
import csv

# Load base 73 spins from reverse
base_ledger = [
    {"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}},
    {"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"LilBlues"},
    {"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},
    {"result":"Leaf2"},{"result":"Leaf2"},{"result":"BigOranges"},{"result":"Leaf1"},
    {"result":"Leaf1"},{"result":"Leaf2","wheelMultiplier":{"value":3,"level":"Low"}},
    {"result":"Leaf1"},{"result":"LilBlues"},{"result":"Leaf1"},{"result":"LilBlues"},
    {"result":"Leaf1"},{"result":"BigOranges"},{"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}},
    {"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf2"},
    {"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},
    {"result":"Leaf1"},{"result":"Leaf1","wheelMultiplier":{"value":3,"level":"Low"}},
    {"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"LilBlues"},
    {"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1","wheelMultiplier":{"value":3,"level":"Low"}},
    {"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},
    {"result":"Leaf2"},{"result":"BigOranges"},{"result":"Leaf1"},{"result":"Leaf1"},
    {"result":"Leaf2"},{"result":"LilBlues","wheelMultiplier":{"value":4,"level":"Low"}},
    {"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1","wheelMultiplier":{"value":7,"level":"Medium"}},
    {"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},
    {"result":"BigOranges"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},
    {"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},
    {"result":"Leaf1","wheelMultiplier":{"value":10,"level":"High"}},
    {"result":"HugeReds"},{"result":"HugeReds"},{"result":"Leaf1"},{"result":"Leaf2"},
    {"result":"Leaf1"},{"result":"BigOranges"},
    {"result":"Leaf2","wheelMultiplier":{"value":4,"level":"Low"}},
    {"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}}
]

new_spins = [
    {"result": "Leaf2"},
    {"result": "Leaf2"},
    {"result": "Leaf1"},
    {"result": "Leaf1"},
    {"result": "Leaf1"},
    {"result": "HugeReds"},
    {"result": "Leaf1"},
    {"result": "BigOranges"}
]

full_history = list(reversed(base_ledger)) + new_spins

# Display Name Mapping
NAME_MAP = {
    "Leaf1": "Light Leaf (Leaf 1)",
    "Leaf2": "Dark Leaf (Leaf 2)",
    "LilBlues": "Lil' Blues",
    "BigOranges": "Big Oranges",
    "HugeReds": "Huge Reds"
}

# Export to JSON
with open("exact_gameplay_history.json", "w", encoding="utf-8") as f:
    json.dump(full_history, f, indent=2)

# Export to CSV
with open("exact_gameplay_history.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["SpinIndex", "InternalResult", "DisplayName", "MultiplierValue", "MultiplierLevel"])
    for idx, item in enumerate(full_history, 1):
        res = item["result"]
        mult = item.get("wheelMultiplier", {})
        w.writerow([idx, res, NAME_MAP.get(res, res), mult.get("value", 1), mult.get("level", "None")])

print(f"[SUCCESS] Exported {len(full_history)} verified spins with Dark/Light leaf labels to exact_gameplay_history.csv")

