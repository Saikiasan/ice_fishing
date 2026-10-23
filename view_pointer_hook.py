with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('Math.sqrt((i.current.x-t.clientX)**2+(i.current.y-t.clientY)**2)<30&&O(t)')
print(c[pos-300:pos+200])
