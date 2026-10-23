with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect MM rendering and add console.log to pointer events or onClick
old_hook = 'I=Z.useCallback(y_.A(()=>{e($)},100),[$]),[R,H]=function(t,O){'
print("Found old_hook:", old_hook in c)

pos = c.find('E=Z.useCallback(t=>{$?.(t),O.bets.placeBet(t)},[O,$])')
print("Found E callback in FM:", pos != -1)
if pos != -1:
    print(c[pos:pos+200])
