with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Patch desktop balance container z:
target1 = 'z={currencySymbol:$.currency.symbol,amount:c??L,'
rep1 = 'z={currencySymbol:$.currency.symbol,amount:(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:(c??L)),'
assert target1 in code, "target1 not found"
code = code.replace(target1, rep1, 1)

# 2. Patch mobile/header balance container 22359:
target2 = 'mAbstractGameContext:!0}),M=l.d4(G.TY),'
rep2 = 'mAbstractGameContext:!0}),M=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:l.d4(G.TY)),'
assert target2 in code, "target2 not found"
code = code.replace(target2, rep2, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully injected reactive live balance directly into Balance UI containers!")
