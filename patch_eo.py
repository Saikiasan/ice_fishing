with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'function EO(t,O){x.h5(()=>{const{state:$}=t.payload,'
replacement = 'function EO(t,O){if(t?.payload?.state?.balance!==undefined){window.__LIVE_BALANCE__=Number(t.payload.state.balance);}x.h5(()=>{const{state:$}=t.payload,'

assert target in code, "Target not found in skipper.js"
new_code = code.replace(target, replacement, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Successfully injected balance synchronization directly into skipper EO handler!")
