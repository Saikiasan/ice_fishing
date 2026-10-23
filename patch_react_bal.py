with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect:
# const x=N.forwardRef((c,h)=>{const s=W.q({allowToConsumeCustomAbstractGameContext:!0}),M=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:l.d4(G.TY)),
old_chunk = 'const x=N.forwardRef((c,h)=>{const s=W.q({allowToConsumeCustomAbstractGameContext:!0}),M=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:l.d4(G.TY)),'

new_chunk = 'const x=N.forwardRef((c,h)=>{const[,_forceUpdate]=N.useState(0);N.useEffect(()=>{const h=()=>_forceUpdate(n=>n+1);window.addEventListener("live_balance_changed",h);return()=>window.removeEventListener("live_balance_changed",h);},[]);const s=W.q({allowToConsumeCustomAbstractGameContext:!0}),M=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:l.d4(G.TY)),'

print("found old_chunk:", old_chunk in c)
if old_chunk in c:
    c = c.replace(old_chunk, new_chunk, 1)
    with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully added live_balance_changed listener to React Balance component!")
