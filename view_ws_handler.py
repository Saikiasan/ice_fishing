import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('async def handle_ws_client')
print(c[pos:pos+1500])
