with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

bad = 'console.log("[DEBUG FM render] betCode:", t.betCode, "isClickBlocked:", O.ui.betSpot.getIsClickBlocked(t.betCode), "isBettingEnabled:", O.bets.isBettingEnabled);c={'
good = 'c={'

c = c.replace(bad, good, 1)

with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Cleaned up FM comma declaration")
