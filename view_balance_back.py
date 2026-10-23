with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('r.displayName="Balance"')
print(c[pos-3000:pos-1500])
