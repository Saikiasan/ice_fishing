with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('addFrameAndCreateLayeredContainer')
p_fn = c.rfind('addFrameAndCreateLayeredContainer(', 0, pos)
if p_fn == -1:
    import re
    m = re.search(r'addFrameAndCreateLayeredContainer\s*\(', c)
    if m: p_fn = m.start()
print('Found at:', p_fn)
print(c[p_fn:p_fn+800])
