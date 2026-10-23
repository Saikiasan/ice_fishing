with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = ';case f.eT.Settled:!function(t,O){const{acceptedBets:$,winType:Z}=t,i=Object.values($).reduce((k=tO.Payout,(t,O)=>{const $=O?.[k];return $?t+$:t}),0);var k;O.result.setPayout({amount:i,level:at(Z)}),O.result.setChipWinAmount(i)}($,O)'
assert target in code, "Target not found in skipper.js!"

# Robust replacement that handles both nested objects and numbers, and sets live balance if present
replacement = ';case f.eT.Settled:!function(t,O){const{acceptedBets:$,winType:Z,totalPayout:tp}=t;let i=0;if(typeof tp==="number")i=tp;else if($){i=Object.values($).reduce((k=tO.Payout,(t,O)=>{const $=typeof O==="number"?O:O?.[k];return $?t+$:t}),0);}var k;const lvl=at(Z)||"Small";O.result.setPayout({amount:i,level:lvl});O.result.setChipWinAmount(i);if(typeof t.balance==="number"){window.__LIVE_BALANCE__=t.balance;if(O.abstractGame?.balance?.setBalance)O.abstractGame.balance.setBalance(t.balance);}}($,O)'

new_code = code.replace(target, replacement, 1)
with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)
print('Successfully patched skipper.js Settled handler!')
