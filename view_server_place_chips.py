import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('msg_type == "icefishing.placeChips"')
print(c[pos-50:pos+1500])
