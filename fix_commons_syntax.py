with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    code = f.read()

pos = code.find(',,Z=c')
print('Found double comma at:', pos)
new_code = code[:pos] + ',' + code[pos+2:]

# Ensure semicolon before function g(c)
g_pos = new_code.find('50000}function g(c)')
if g_pos != -1:
    new_code = new_code[:g_pos] + '50000};function g(c)' + new_code[g_pos+len('50000}function g(c)'):]

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(new_code)
print('Successfully fixed commons.js!')
