with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('for(const c of this.frames)switch(c.layout){case F.E.Fill:')
print(c[pos:pos+300])
