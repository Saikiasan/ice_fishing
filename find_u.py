with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f: c = f.read()
pos = c.find('return nO.A(Z)?{bet:i,resultsMap:{}}:{bet:nO.A(i)?void 0:i,resultsMap:Z}')
print('v$ return pos:', pos)
print(c[pos-200:pos+150])
