with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_code = '''            f_mult = forced.get("multiplier", 1)
            if str(f_mult).lower() == "random":
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = int(f_mult)'''

new_code = '''            f_mult = forced.get("multiplier", 1)
            if str(f_mult).lower() == "random" or (int(f_mult) <= 1 and winning_result in ["LilBlues", "BigOranges", "HugeReds"]):
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = int(f_mult)'''

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    with open('evo_backend_server.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully updated forced fish multiplier logic!")
else:
    print("Could not find old_code")
