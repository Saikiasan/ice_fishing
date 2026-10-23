with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

bad = 'const _bal=(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c);const a='
good = 'a="number"==typeof(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c)?o.ej((typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c),{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"'

# let's replace back to clean expression
pos = c.find('const _bal=')
end = c.find(':" -"', pos) + len(':" -"')
print("Found chunk:", c[pos:end])

c = c[:pos] + 'a="number"==typeof(typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c)?o.ej((typeof window.__LIVE_BALANCE__==="number"?window.__LIVE_BALANCE__:c),{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"' + c[end:]

with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully cleaned up Balance expression in commons.js!")
