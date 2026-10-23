with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

pos = code.find('__LIVE_BALANCE__')
start = code.rfind('Z=', 0, pos)
end = code.find(';function g(c)', pos)
print('Current Z definition:', repr(code[start:end]))

replacement = 'Z=L(n,c=>{const s=window.__LIVE_BALANCE__;if(typeof s==="number"&&!isNaN(s))return s;return typeof c==="number"&&!isNaN(c)?c:50000})'
new_code = code[:start] + replacement + code[end:]

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Done converting Z to reactive Redux selector!')
