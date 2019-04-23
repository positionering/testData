import numpy as np
import pandas as pd

data = np.ndarray((100000,5))

with open('testlogs/wodometry_test_sixth90normal') as f:

    for i, line in enumerate(f):
        for j, value in enumerate(line.split()):
            # if i == 0:
               # data[i,j] = value.split(':')[0]
            data[i,j] = value.split(':')[1]
            
print(data)