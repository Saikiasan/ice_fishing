with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'function jt(t){const O=new Set(function(t){const O=[];for(const $ of Object.keys(t)){const Z=t[$];Z&&O.push(Z.error.code)}return O}(t.invalidBets));return t.errorCode&&O.add(t.errorCode),O}'
replacement = 'function jt(t){const O=new Set(function(t){const O=[];if(!t||!t.invalidBets)return O;for(const $ of Object.keys(t.invalidBets)){const Z=t.invalidBets[$];Z&&O.push(Z.error.code)}return O}(t));return t&&t.errorCode&&O.add(t.errorCode),O}'

assert target in code, "Target jt not found in skipper.js"
new_code = code.replace(target, replacement, 1)

with open('d:/Codes/ice_fishing/evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Successfully patched jt function in skipper.js!")
