with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'DeviceSupport\s*=\s*', c)]
if not matches:
    matches = [m.start() for m in re.finditer(r'IS_DESKTOP\s*:', c)]
print('Matches for DeviceSupport/IS_DESKTOP definition:', len(matches))
for m in matches[:5]:
    print(c[max(0, m-80):min(len(c), m+250)])
    print('='*50)
