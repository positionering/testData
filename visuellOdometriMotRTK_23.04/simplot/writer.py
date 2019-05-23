from time import sleep
with open("logtest.txt", 'w') as f:
    for i in range(10):
        f.write(str(i) + '\n')
        f.flush()
        sleep(1)