with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'const Z=t.payload.timeRemaining-$'
replacement = 'const Z=t.payload.timeRemaining-(typeof $=="number"?$:0)'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully patched betsOpen in skipper.v0.973337fc.js!')
else:
    print('Target not found!')
