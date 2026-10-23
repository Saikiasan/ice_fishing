with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'pauseBalanceUpdate', c)]
for m in matches:
    print(c[max(0, m-100):min(len(c), m+200)])
    print('='*50)
