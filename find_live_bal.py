with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('__LIVE_BALANCE__')
while pos != -1:
    print('Found at', pos)
    print(c[max(0, pos-100):min(len(c), pos+150)])
    print('='*50)
    pos = c.find('__LIVE_BALANCE__', pos+1)
