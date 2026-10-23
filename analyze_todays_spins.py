import json
from collections import Counter

raw_results = [
    {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf1"},
    {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf1"},
    {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf1"},
    {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf2"},
    {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf2"},
    {"result": "Leaf1", "wheelMultiplier": {"value": 4, "level": "Low"}},
    {"result": "LilBlues"},
    {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf1"},
    {"result": "LilBlues"},
    {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf2"},
    {"result": "Leaf1", "wheelMultiplier": {"value": 3, "level": "Low"}},
    {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf2"},
    {"result": "Leaf2"},
    {"result": "Leaf2", "wheelMultiplier": {"value": 4, "level": "Low"}},
    {"result": "Leaf1", "wheelMultiplier": {"value": 3, "level": "Low"}},
    {"result": "Leaf1"}, {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf1"},
    {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf2"},
    {"result": "Leaf2"},
    {"result": "LilBlues", "wheelMultiplier": {"value": 2, "level": "Low"}},
    {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf2"}, {"result": "Leaf2"},
    {"result": "LilBlues"},
    {"result": "BigOranges", "wheelMultiplier": {"value": 2, "level": "Low"}},
    {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf2"},
    {"result": "Leaf1", "wheelMultiplier": {"value": 5, "level": "Medium"}},
    {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf1"},
    {"result": "Leaf1", "wheelMultiplier": {"value": 4, "level": "Low"}},
    {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf1"},
    {"result": "Leaf1"}, {"result": "Leaf2"}, {"result": "Leaf1"}, {"result": "Leaf1"},
    {"result": "Leaf2"}, {"result": "Leaf2"}
]

total = len(raw_results)
counts = Counter(r["result"] for r in raw_results)

print(f"Total delivered rounds: {total}")
print("\n" + "="*50)
print("TODAY'S OUTCOME DISTRIBUTION (LAST 73 SPINS):")
print("="*50)
for k, v in counts.most_common():
    label = "Light Leaf (L1)" if k == "Leaf1" else "Dark Leaf (L2)" if k == "Leaf2" else k
    print(f"  {label:18} ({k:10}): {v:2d} ({v/total*100:5.1f}%)")

mults = [r for r in raw_results if "wheelMultiplier" in r]
print("\n" + "="*50)
print(f"MULTIPLIERS HIT: {len(mults)} / {total} ({len(mults)/total*100:.1f}%)")
print("="*50)
for m in mults:
    k = m["result"]
    label = "Light Leaf (L1)" if k == "Leaf1" else "Dark Leaf (L2)" if k == "Leaf2" else k
    print(f"  {label:18} -> {m['wheelMultiplier']['value']}x ({m['wheelMultiplier']['level']})")

print("\n" + "="*50)
print("DROUGHT ANALYSIS (Rounds since last appearance):")
print("="*50)
for fish in ["HugeReds", "BigOranges", "LilBlues", "Leaf2", "Leaf1"]:
    drought = next((i for i, r in enumerate(raw_results) if r.get("result") == fish), total)
    name = "Huge Reds" if fish == "HugeReds" else "Big Oranges" if fish == "BigOranges" else "Lil' Blues" if fish == "LilBlues" else fish
    print(f"  {name:18}: {drought:2d} rounds ago")

# Streak analysis at current head (index 0 is the newest round)
current_streak_item = raw_results[0]["result"]
current_streak_len = 0
for r in raw_results:
    if r["result"] == current_streak_item:
        current_streak_len += 1
    else:
        break

print(f"\nActive Newest Streak: {current_streak_len}x consecutive {current_streak_item} ('Light Leaf')")
