with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('c={...t,setReference:k,isClickBlocked:O.ui.betSpot.getIsClickBlocked(t.betCode),onClick:E};')
print(c[pos-600:pos])
