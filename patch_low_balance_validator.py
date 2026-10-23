with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = ',(t,O)=>{const{bet:$,betCodes:Z}=t,i=v($),k={};if(O.abstractGame.balance.available<i)for(const t of Z)k[t]={type:i$.Error,betCode:t,payload:{code:k$.LowBalance}};return k}'
# Bypass LowBalance block if balance.available was not updated by Redux (use window.__LIVE_BALANCE__ or allow)
replacement = ',(t,O)=>{const{bet:$,betCodes:Z}=t,i=v($),k={};const avail=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:O.abstractGame.balance.available);if(avail<i)for(const t of Z)k[t]={type:i$.Error,betCode:t,payload:{code:k$.LowBalance}};return k}'

assert target in code, "Target not found in skipper.js"
new_code = code.replace(target, replacement, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Successfully patched LowBalance validator in skipper.js!")
