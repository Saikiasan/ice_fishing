with open('evo_server/frontend/evo/r3/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'const t="service.worker.600e75c8.js";'
print('target in c:', target in c)
if target in c:
    c = c.replace(target, 'return;const t="service.worker.600e75c8.js";')
    with open('evo_server/frontend/evo/r3/index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Disabled service worker!')
