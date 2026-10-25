with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'IS_DESKTOP', c)]
print('Matches for IS_DESKTOP in commons:', len(matches))
for m in matches[:10]:
    print(c[max(0, m-80):min(len(c), m+180)])
    print('='*50)
