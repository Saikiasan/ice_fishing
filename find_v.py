with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
pos = c.find('function v$(')
if pos == -1:
    m = re.search(r'v\$\s*=', c)
    if m:
        pos = m.start()

print('v$ position:', pos)
if pos != -1:
    print(c[pos:pos+800])
