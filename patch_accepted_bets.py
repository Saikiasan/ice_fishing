with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'case f.eT.Accepted:!function(t,O){const{chips:$}=t;Tt(function(t){return S({type:h.ClientBetAccepted,payload:{bets:t},enhancers:r})}($),O)}($,O);break;'
assert target in code, "Target not found in skipper.js!"

replacement = 'case f.eT.Accepted:!function(t,O){const{chips:$}=t;if(typeof t.balance==="number"){window.__LIVE_BALANCE__=t.balance;if(O.abstractGame?.balance?.setBalance)O.abstractGame.balance.setBalance(t.balance);}Tt(function(t){return S({type:h.ClientBetAccepted,payload:{bets:t},enhancers:r})}($),O)}($,O);break;'

new_code = code.replace(target, replacement, 1)
with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)
print('Successfully patched skipper.js Accepted bet balance handler!')
