with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'return{totalBet:c.layout.totalBet,'
replacement = 'return{totalBet:(typeof window.__TOTAL_BET__==="number"?window.__TOTAL_BET__:c.layout.totalBet),'

assert target in code, "Target not found in commons.js"
new_code = code.replace(target, replacement, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Successfully patched totalBet in B component!")
