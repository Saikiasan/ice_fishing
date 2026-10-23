import json
from collections import Counter

# First packet contains the base ledger (73 spins)
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

# The next 8 consecutive spins you captured:
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

# Total chronology (81 spins)
full_history = list(reversed(base_ledger)) + new_spins

print(f"Total verified chronological spins: {len(full_history)}")
counts = Counter(r["result"] for r in full_history)

print("\n" + "="*50)
print("TOTAL VERIFIED RESULTS BREAKDOWN (81 SPINS):")
print("="*50)
for k, v in counts.most_common():
    print(f"{k:12}: {v:2d} ({v/len(full_history)*100:5.1f}%)")

mults = [r for r in full_history if "wheelMultiplier" in r]
print(f"\nMultipliers hit: {len(mults)} ({len(mults)/len(full_history)*100:.1f}%)")
for m in mults:
    print(f"  {m['result']} -> {m['wheelMultiplier']['value']}x ({m['wheelMultiplier']['level']})")
