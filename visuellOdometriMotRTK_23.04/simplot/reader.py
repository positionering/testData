import matplotlib.pyplot as plt 
import numpy as np 
import time

def follow(thefile):
    # thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line

with open("logtest.txt", 'r') as log:
    for i in follow(log):
        print(i)


# x = data[:,0]
# y = data[:,1]

# print(x, y)
