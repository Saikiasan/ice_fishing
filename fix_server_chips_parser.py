with open('evo_backend_server.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_code = '''                # 2. Handle bet placement: icefishing.placeChips
                elif msg_type == "icefishing.placeChips":
                    incoming_chips = payload.get("chips") or payload.get("bet") or {}
                    if not incoming_chips and isinstance(payload, dict):
                        for k, v in payload.items():
                            if k in ["Leaf1", "Leaf2", "LilBlues", "BigOranges", "HugeReds"]:
                                incoming_chips[k] = v

                    for bet_spot, amt in incoming_chips.items():
                        game_control_state["current_bets"][bet_spot] = amt

                    total_bet = sum(game_control_state["current_bets"].values())
                    # Persistent balance deduction from committed_balance
                    game_control_state["balance"] = max(0.0, game_control_state["committed_balance"] - total_bet)
                    print(f"[BET RECEIVED] Active Bets: {game_control_state['current_bets']} | Total Bet: ₹{total_bet} | Live Balance: ₹{game_control_state['balance']}")'''

new_code = '''                # 2. Handle bet placement: icefishing.placeChips
                elif msg_type == "icefishing.placeChips":
                    args = payload.get("args") if isinstance(payload.get("args"), dict) else {}
                    incoming_chips = (
                        args.get("chips") or
                        args.get("bet") or
                        payload.get("chips") or
                        payload.get("bet") or
                        data.get("args", {}).get("chips") or
                        data.get("args", {}).get("bet") or
                        {}
                    )
                    if not incoming_chips and isinstance(payload, dict):
                        for k, v in payload.items():
                            if k in ["Leaf1", "Leaf2", "LilBlues", "BigOranges", "HugeReds"]:
                                incoming_chips[k] = v

                    for bet_spot, amt in incoming_chips.items():
                        game_control_state["current_bets"][bet_spot] = amt

                    total_bet = sum(game_control_state["current_bets"].values())
                    # Dynamic balance deduction from committed_balance
                    game_control_state["balance"] = max(0.0, game_control_state["committed_balance"] - total_bet)
                    print(f"[BET RECEIVED] Active Bets: {game_control_state['current_bets']} | Total Bet: ₹{total_bet} | Live Balance: ₹{game_control_state['balance']}")'''

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    with open('evo_backend_server.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully updated incoming_chips parser in evo_backend_server.py!")
else:
    print("Could not find old_code")
