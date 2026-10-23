with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = """                outer_id = data.get("id")
                recipient = data.get("recipient")
                payload = data.get("payload") if isinstance(data.get("payload"), dict) else data
                inner_id = payload.get("id") if isinstance(payload, dict) else None
                msg_type = payload.get("type") or data.get("type")"""

new_block = """                outer_id = data.get("id")
                recipient = data.get("recipient")
                payload = data.get("payload") if isinstance(data.get("payload"), dict) else data
                inner_id = payload.get("id") if isinstance(payload, dict) else None
                msg_type = payload.get("type") or data.get("type")
                if msg_type not in ["metrics.ping", "ping"]:
                    print(f"[WS INCOMING] type={msg_type} recipient={recipient} payload={payload}")"""

if old_block in c:
    c = c.replace(old_block, new_block, 1)
    with open('evo_backend_server.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully added WS INCOMING log!")
else:
    print("old_block not found")
