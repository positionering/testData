x = 0
y = 0

with open("logtest.txt", 'w') as f:
    while x != 10000:
        f.write(str(x) + ' ' + str(y) + '\n')
        y += 0.5
        x += 1

