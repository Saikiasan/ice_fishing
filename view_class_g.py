with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('class G{')
if pos == -1: pos = c.find('new G(this,this.loader')
p_cls = c.rfind('class G', 0, pos)
print(c[p_cls:p_cls+1000])
