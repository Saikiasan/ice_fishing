with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
pos = c.find('isBettingEnabled')
while pos != -1:
    print('Found isBettingEnabled at', pos)
    print(c[max(0, pos-100):min(len(c), pos+150)])
    print('='*50)
    pos = c.find('isBettingEnabled', pos+1)
