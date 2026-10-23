with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

# In FM:
old_fm = 'c={...t,setReference:k,isClickBlocked:O.ui.betSpot.getIsClickBlocked(t.betCode),onClick:E};'
new_fm = 'console.log("[DEBUG FM render] betCode:", t.betCode, "isClickBlocked:", O.ui.betSpot.getIsClickBlocked(t.betCode), "isBettingEnabled:", O.bets.isBettingEnabled);c={...t,setReference:k,isClickBlocked:O.ui.betSpot.getIsClickBlocked(t.betCode),onClick:E};'

# And in MM:
old_mm = 'I=Z.useCallback(y_.A(()=>{e($)},100),[$]),'
new_mm = 'I=Z.useCallback(y_.A(()=>{console.log("[DEBUG MM onClick trigger] for betCode:", $);e($)},100),[$]),'

# And in pointerup hook:
old_ptr = 'Math.sqrt((i.current.x-t.clientX)**2+(i.current.y-t.clientY)**2)<30&&O(t)'
new_ptr = 'console.log("[DEBUG MM pointerup] dist:", Math.sqrt((i.current.x-t.clientX)**2+(i.current.y-t.clientY)**2), "active:", $.current),Math.sqrt((i.current.x-t.clientX)**2+(i.current.y-t.clientY)**2)<30&&O(t)'

c = c.replace(old_fm, new_fm, 1)
c = c.replace(old_mm, new_mm, 1)
c = c.replace(old_ptr, new_ptr, 1)

with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added debug logs in FM, MM, and pointerup!")
