with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('getDimensionsAndLayoutFrames')
p_cls = c.rfind('class ', 0, pos)
print(c[p_cls:p_cls+2000])
