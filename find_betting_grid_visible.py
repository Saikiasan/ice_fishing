with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect where bettingGrid.visible is set or defined
import re
for m in re.finditer(r'bettingGrid\.visible', c):
    print(c[max(0, m.start()-50):min(len(c), m.start()+100)])
    print('='*50)
