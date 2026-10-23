with open('evo_server/frontend/evo/r3/js/skipper.v0.973337fc.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('aO.iB(t=>!this.rootStore.ui.bettingGrid.visible||this.rootStore.draggableChip.isChipDraggedFor(t))')
print("Found bettingGrid.visible check:", pos != -1)
if pos != -1:
    print(c[pos-50:pos+150])
