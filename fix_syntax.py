with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

bad = 'placeBet(t){console.log("[DEBUG placeBet] called for", t, "lastSelectedAmount:", this.rootStore.abstractGame.betAmounts.lastSelectedAmount, "phase:", this.rootStore.gamePhase.phase, "isBettingEnabled:", this.isBettingEnabled);const O=this.rootStore.abstractGame.betAmounts.lastSelectedAmount,$=v$({[t]:O},this.rootStore);console.log("[DEBUG placeBet] validation result:", $);{bet:Z,resultsMap:i}=$,k=f.uu.Chip;'
good = 'placeBet(t){console.log("[DEBUG placeBet] called for", t, "lastSelectedAmount:", this.rootStore.abstractGame.betAmounts.lastSelectedAmount, "phase:", this.rootStore.gamePhase.phase, "isBettingEnabled:", this.isBettingEnabled);const O=this.rootStore.abstractGame.betAmounts.lastSelectedAmount,$=v$({[t]:O},this.rootStore);console.log("[DEBUG placeBet] validation result:", $);const{bet:Z,resultsMap:i}=$,k=f.uu.Chip;'

if bad in c:
    c = c.replace(bad, good, 1)
    with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed syntax error in skipper.js!")
else:
    print("bad pattern not found")
