import matplotlib.pyplot as plt 
import numpy as np 

data = np.loadtxt("logtest.txt")

x = data[:,0]
y = data[:,1]

print(x, y)