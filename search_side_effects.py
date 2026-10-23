with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
funcs = ['GO', 'oO', 'q$', 'J$', 'D$', 'w$', 'S$', 'mZ', 'qO', 'r$', 'K$']
for fn in funcs:
    pos = c.find(f'function {fn}(')
    if pos != -1:
        snippet = c[pos:pos+250]
        if 'balance' in snippet or 'result' in snippet or 'payout' in snippet or 'Settled' in snippet:
            print(f'=== {fn} ===')
            print(snippet)
