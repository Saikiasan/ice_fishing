with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('getIsClickBlocked')
while pos != -1:
    print('getIsClickBlocked at', pos)
    print(c[max(0, pos-100):min(len(c), pos+200)])
    print('='*50)
    pos = c.find('getIsClickBlocked', pos+1)
