with open('evo_server/frontend/evo/r3/js/commons.a527ac5d.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = 2378944
old_expr = 'a="number"==typeof c?o.ej(c,{currencySymbol:l||s?void 0:h,decimalThreshold:w}):" -"'
print("Found old_expr:", old_expr in c)
if old_expr in c:
    print(c[pos-50:pos+120])
