with open('evo_server/frontend/evo/r3/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect around </head>
pos = c.find('</head>')
print(c[pos-200:pos+50])
