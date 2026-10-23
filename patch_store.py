with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'function zE(){const t=Z.useContext(fE);if(!t)throw new Error("Store should be provided to StoreContext");return t}'
replacement = 'function zE(){const t=Z.useContext(fE);if(!t)throw new Error("Store should be provided to StoreContext");window.__STORE__=t;return t}'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully exposed window.__STORE__ in skipper!')
else:
    print('Target not found')
