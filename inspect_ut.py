with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
m = re.search(r'\bIO\s*=\s*function\(t\)\{([^}]+)\}\(\{\}\)', c)
if m:
    print('IO:', m.group(1))
else:
    pos = c.find('IO=')
    print(c[pos:pos+200])
