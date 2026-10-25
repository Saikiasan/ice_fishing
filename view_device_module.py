with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('DeviceProperties:()=>s,IS_PHONE:()=>s.platform===F.OD.Phone')
print(c[pos-200:pos+300])
