with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('33299(c,h,s){')
print(c[pos:pos+1500])
