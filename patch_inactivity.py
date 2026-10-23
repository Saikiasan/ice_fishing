with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'return s&&h!==G.b.KickOut&&M.jsxs("div",{className:L,"data-role":"inactivity-message-wrapper"'
replacement = 'return !1&&M.jsxs("div",{className:L,"data-role":"inactivity-message-wrapper"'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully eliminated inactivity wrapper rendering!')
else:
    print('Target not found')
