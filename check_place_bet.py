with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
pos = c.find('placeBet(t){')
print(c[pos:pos+400])
