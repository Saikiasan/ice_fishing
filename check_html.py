import re

with open('official_assets/index_evo_r3.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)', html)
styles = re.findall(r'<link[^>]*href=[\'"]([^\'"]+\.css[^\'"]*)', html)

print('Scripts:')
for s in scripts:
    print(' ', s)

print('\nStyles:')
for st in styles:
    print(' ', st)
