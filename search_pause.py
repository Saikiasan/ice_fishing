with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'pause', c, re.IGNORECASE)]
print('Total "pause":', len(matches))
for m in matches:
    snippet = c[max(0, m-50):min(len(c), m+150)]
    if 'balance' in snippet.lower():
        print(snippet)
        print('='*50)
