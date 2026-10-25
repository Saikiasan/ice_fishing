with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('getDimensionsAndLayoutFrames=')
if pos == -1: pos = c.find('getDimensionsAndLayoutFrames')
print(c[pos-200:pos+800])
