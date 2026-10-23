with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = '''        else:
            winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            target_mult = 1'''

new_block = '''        else:
            winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            # If a fish is caught, always assign a multiplier!
            if winning_result in ["LilBlues", "BigOranges", "HugeReds"]:
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = 1'''

if old_block in c:
    c = c.replace(old_block, new_block, 1)
    with open('evo_backend_server.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully updated fish caught multiplier logic!")
else:
    print("Could not find old_block")
