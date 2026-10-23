with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's add console.log inside placeBet:
old_place_bet = 'placeBet(t){const O=this.rootStore.abstractGame.betAmounts.lastSelectedAmount,$=v$({[t]:O},this.rootStore),'
new_place_bet = 'placeBet(t){console.log("[DEBUG placeBet] called for", t, "lastSelectedAmount:", this.rootStore.abstractGame.betAmounts.lastSelectedAmount, "phase:", this.rootStore.gamePhase.phase, "isBettingEnabled:", this.isBettingEnabled);const O=this.rootStore.abstractGame.betAmounts.lastSelectedAmount,$=v$({[t]:O},this.rootStore);console.log("[DEBUG placeBet] validation result:", $);'

if old_place_bet in c:
    c = c.replace(old_place_bet, new_place_bet, 1)
    with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully instrumented placeBet!")
else:
    print("Could not find old_place_bet")
