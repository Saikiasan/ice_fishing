with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('a="number"==typeof c?o.ej(c,{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"')
print(pos)
if pos != -1:
    print(c[pos-100:pos+200])
