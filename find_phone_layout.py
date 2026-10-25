with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'componentLayout===V\.Phone', c)]
print('Matches for Phone:', len(matches))
for m in matches:
    print(c[max(0, m-80):min(len(c), m+180)])
    print('='*50)
