with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update GET /api/outcome
old_get_outcome = '''        # API: Query or GET set outcome (easy via browser URL bar)
        # e.g.: /api/outcome?result=LilBlues&mult=4
        if path == "/api/outcome":
            target = query.get("result", [None])[0]
            mult = query.get("mult", [1])[0]
            if target:
                game_control_state["forced_next_outcome"] = {
                    "result": target,
                    "multiplier": int(mult)
                }
                print(f"\\n[ADMIN GET] Next round FORCED to: {game_control_state['forced_next_outcome']}\\n")'''

new_get_outcome = '''        # API: Query or GET set outcome (easy via browser URL bar)
        # e.g.: /api/outcome?result=LilBlues&mult=4 or /api/outcome?result=BigOranges&mult=random
        if path == "/api/outcome":
            target = query.get("result", [None])[0]
            mult = query.get("mult", [1])[0]
            if target:
                mult_val = "random" if str(mult).lower() == "random" else int(mult)
                game_control_state["forced_next_outcome"] = {
                    "result": target,
                    "multiplier": mult_val
                }
                print(f"\\n[ADMIN GET] Next round FORCED to: {game_control_state['forced_next_outcome']}\\n")'''

# 2. Update POST /api/set_next_outcome
old_post_outcome = '''                target_result = data.get("result") # Leaf1, Leaf2, LilBlues, BigOranges, HugeReds
                multiplier = data.get("multiplier", 1)
                if target_result:
                    game_control_state["forced_next_outcome"] = {
                        "result": target_result,
                        "multiplier": int(multiplier) if multiplier else 1
                    }'''

new_post_outcome = '''                target_result = data.get("result") # Leaf1, Leaf2, LilBlues, BigOranges, HugeReds
                multiplier = data.get("multiplier", 1)
                if target_result:
                    mult_val = "random" if str(multiplier).lower() == "random" else (int(multiplier) if multiplier else 1)
                    game_control_state["forced_next_outcome"] = {
                        "result": target_result,
                        "multiplier": mult_val
                    }'''

# 3. Update game loop handling of forced outcome multiplier
old_loop_outcome = '''        if forced and forced.get("result"):
            target_res = forced["result"]
            matching_indices = [idx for idx, sec in enumerate(WHEEL_SECTORS) if sec.lower() == target_res.lower()]
            if matching_indices:
                winning_sector = random.choice(matching_indices)
            else:
                winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            target_mult = int(forced.get("multiplier", 1))
        else:'''

new_loop_outcome = '''        if forced and forced.get("result"):
            target_res = forced["result"]
            matching_indices = [idx for idx, sec in enumerate(WHEEL_SECTORS) if sec.lower() == target_res.lower()]
            if matching_indices:
                winning_sector = random.choice(matching_indices)
            else:
                winning_sector = random.randint(0, 52)
            winning_result = WHEEL_SECTORS[winning_sector]
            f_mult = forced.get("multiplier", 1)
            if str(f_mult).lower() == "random":
                target_mult = random.choice([2, 3, 4, 5, 7, 10, 15, 20, 25, 50, 100])
            else:
                target_mult = int(f_mult)
        else:'''

c = c.replace(old_get_outcome, new_get_outcome, 1)
c = c.replace(old_post_outcome, new_post_outcome, 1)
c = c.replace(old_loop_outcome, new_loop_outcome, 1)

with open('evo_backend_server.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully updated evo_backend_server.py for random multiplier!")
