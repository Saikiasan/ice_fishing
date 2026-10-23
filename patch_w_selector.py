with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'w=L(J,c=>{let h,s=0;return c.forEach(({serverBalance:c,serverBalanceVersion:V=0})=>{V>=s&&(h=c,s=V)}),h})'
assert target in code, "Target not found in commons.js"

# Robust w selector:
replacement = 'w=L(W,c=>{if(Array.isArray(c)){for(const t of c){if(t&&typeof t.serverBalance==="number")return t.serverBalance;}}return void 0})'

new_code = code.replace(target, replacement, 1)
with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Successfully patched w selector in commons.js!')
