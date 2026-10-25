with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('get componentLayout(){return this.DS.IS_DESKTOP?this.isClassicLayout?V.DesktopClassic:V.Desktop:this.DS.IS_TABLET?V.Tablet:V.Phone}')
print(pos)
print(c[pos-100:pos+250])
