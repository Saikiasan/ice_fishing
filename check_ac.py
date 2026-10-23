with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect A$ and c$ right after placeBet
pos = c.find('A$({validationResults:$,validationSource:k,store:this.rootStore})')
print(c[pos-100:pos+300])
