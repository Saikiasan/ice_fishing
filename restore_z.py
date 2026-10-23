with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

pos = code.find('__LIVE_BALANCE__')
start = code.rfind('Z=L(n,', 0, pos)
end = code.find(');function g(c)', pos) + 1
print('Old:', repr(code[start:end]))

replacement = 'Z=L(n,c=>typeof c==="number"&&!isNaN(c)?c:50000)'
new_code = code[:start] + replacement + code[end:]

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Cleanly restored Z=L(n,...) in commons.js!')
