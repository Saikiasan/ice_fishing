with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('f$=[')
if pos == -1:
    pos = c.find('f$=')
print('f$ position:', pos)
if pos != -1:
    print(c[pos:pos+1500])
