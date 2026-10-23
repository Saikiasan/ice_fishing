with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'S=L(n,c=>void 0===c?0:c),Z=n;function g(c){'
replacement = 'S=L(n,c=>void 0===c?0:c),Z=L(n,c=>typeof c=="number"&&!isNaN(c)?c:50000);function g(c){'

if target not in c:
    print('Target not found!')
    exit(1)

c = c.replace(target, replacement, 1)

with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully patched Z in commons.a527ac5d.js!')
