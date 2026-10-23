with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('"data-role":"balance-value"')
print(c[pos-500:pos+250])
