import json
from collections import Counter

raw = """[{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1","wheelMultiplier":{"value":3,"level":"Low"}},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"LilBlues"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"LilBlues"},{"result":"Leaf2"},{"result":"HugeReds"},{"result":"Leaf1"},{"result":"LilBlues"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2","wheelMultiplier":{"value":3,"level":"Low"}},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"BigOranges"},{"result":"Leaf2","wheelMultiplier":{"value":3,"level":"Low"}},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}},{"result":"Leaf1","wheelMultiplier":{"value":4,"level":"Low"}},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf2","wheelMultiplier":{"value":3,"level":"Low"}},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf2"},{"result":"LilBlues"},{"result":"Leaf2","wheelMultiplier":{"value":4,"level":"Low"}},{"result":"Leaf1","wheelMultiplier":{"value":3,"level":"Low"}},{"result":"Leaf2"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"},{"result":"Leaf1"}]"""

results = json.loads(raw)
print(f"Total delivered rounds in spinHistory: {len(results)}")

counts = Counter(r["result"] for r in results)
for k, v in counts.most_common():
    print(f"{k:12}: {v:2d} ({v/len(results)*100:5.1f}%)")

mults = [r for r in results if "wheelMultiplier" in r]
print(f"\nRounds with Wheel Multipliers: {len(mults)} ({len(mults)/len(results)*100:.1f}%)")
for m in mults:
    print(f"  {m['result']} -> {m['wheelMultiplier']['value']}x ({m['wheelMultiplier']['level']})")
