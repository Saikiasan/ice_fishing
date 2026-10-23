with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

pos = code.find('50000')
print('Found 50000 at:', pos)
target = code[pos-41:pos+7]
print('Target:', repr(target))
replacement = ',Z=c=>{const s=window.__LIVE_BALANCE__;if(typeof s==="number"&&!isNaN(s))return s;const b=n(c);return typeof b==="number"&&!isNaN(b)?b:50000}'
new_code = code[:pos-41] + replacement + code[pos+7:]
with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)
print('Successfully patched commons.js!')
