with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('s.platform===F.OD.Phone')
p_mod = c.rfind('(c,h,s){', 0, pos)
print(c[p_mod-30:p_mod+400])
