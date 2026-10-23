with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'function EO(t,O){if(t?.payload?.state?.balance!==undefined){window.__LIVE_BALANCE__=Number(t.payload.state.balance);}'
replacement = '''function EO(t,O){
    if(t?.payload?.state?.balance!==undefined){
        window.__LIVE_BALANCE__=Number(t.payload.state.balance);
    }
    if(t?.payload?.state?.chips){
        const chipsObj=t.payload.state.chips;
        const sumBets=Object.values(chipsObj).reduce((a,b)=>a+(Number(b)||0),0);
        window.__TOTAL_BET__=sumBets;
        if(O.abstractGame?.balance?.setTotalBet){
            O.abstractGame.balance.setTotalBet(sumBets);
        }
    } else if(t?.payload?.state?.status==="NoBets"){
        window.__TOTAL_BET__=0;
        if(O.abstractGame?.balance?.setTotalBet){
            O.abstractGame.balance.setTotalBet(0);
        }
    }
'''

assert target in code, "Target not found in skipper.js"
new_code = code.replace(target, replacement, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Successfully injected total bet reactivity into skipper EO handler!")
