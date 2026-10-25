with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('addFrame(c,h={update:!0})')
print(c[pos:pos+1500])
