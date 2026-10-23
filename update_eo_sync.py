with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('function EO(t,O){')
old_header = '''function EO(t,O){
    if(t?.payload?.state?.balance!==undefined){
        window.__LIVE_BALANCE__=Number(t.payload.state.balance);
    }'''

new_header = '''function EO(t,O){
    if(t?.payload?.state?.balance!==undefined){
        window.__LIVE_BALANCE__=Number(t.payload.state.balance);
        if(O.abstractGame?.balance?.setBalance){
            O.abstractGame.balance.setBalance(Number(t.payload.state.balance));
        }
    }'''

if old_header in c:
    c = c.replace(old_header, new_header, 1)
    with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully updated EO header in skipper.js!")
else:
    print("Could not find old_header")
