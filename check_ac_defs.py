with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('function A$(')
print(c[pos:pos+400])
pos2 = c.find('function c$(')
print(c[pos2:pos2+400])
