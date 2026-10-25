import glob

for f in glob.glob('evo_server/frontend/evo/r3/js/*.js'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if 'IS_TABLET' in c:
        print('Found IS_TABLET in', f)
