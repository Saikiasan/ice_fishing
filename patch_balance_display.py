with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = 2378944
old_str = 'a="number"==typeof c?o.ej(c,{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"'
# Hook `c`: if window.__LIVE_BALANCE__ is defined and a number, use it!
new_str = 'const _bal=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c);const a="number"==typeof _bal?o.ej(_bal,{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"'

if old_str in c:
    c = c.replace(old_str, new_str, 1)
    with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully patched Balance display in commons.js!")
else:
    print("Could not find old_str")
