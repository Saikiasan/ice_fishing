# Check what validators are in f$
with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_f = c.find('f$=[')
pos_end = c.find('z$=[k$.MaxBetLimit];')
print('=== f$ validators ===')
print(c[pos_f:pos_end])
