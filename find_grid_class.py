with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('bettingGrid{')
if pos == -1: pos = c.find('class Oi') # or find bettingGrid
print('pos:', pos)
import re
for m in re.finditer(r'class \w+{get visible\(\)', c):
    print(c[m.start():m.start()+250])
