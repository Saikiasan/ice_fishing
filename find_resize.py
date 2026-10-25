with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'resize', c, re.IGNORECASE)]
print('Matches for resize in commons:', len(matches))
for m in matches[:10]:
    snippet = c[max(0, m-50):min(len(c), m+150)]
    if 'layout' in snippet.lower() or 'game' in snippet.lower() or 'screen' in snippet.lower() or 'error' in snippet.lower():
        print(snippet)
        print('='*50)
