import numpy as np

def array_smoothing(x):
    for i in range(len(x)):
        c = 0
        while i+c < len(x) and x[i+c] == x[i]:
            c += 1
        
        for j in range(c):
            x[i+j] += 1/c * j

    return np.diff(np.array(x))