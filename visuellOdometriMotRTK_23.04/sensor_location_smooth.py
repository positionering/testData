from math import acos, asin, cos, sin, sqrt, atan2, pi
from matplotlib import pyplot as plt
import numpy as np

def array_smoothing(x):
    for i in range(len(x)):
        c = 0
        while i+c < len(x) and x[i+c] == x[i]:
            c += 1
        
        for j in range(c):
            x[i+j] += 1/c * j

    return np.diff(np.array(x))


def wo_location(c_left, c_right, filename):
    dpp = 0.545*math.pi/29
    wdt = 1.08
    campos = 0.9
   
    heading = [math.pi/2] #north
    x = 0
    y = 0.9
    lx= [0] 
    ly = [0.9]
    camx = [0]
    camy = [0]

    c_left_diff = array_smoothing(c_left)
    c_right_diff = array_smoothing(c_right)
    
    i = [i for i, e in enumerate(abs(c_left_diff)) if e > 2]
    j = [j for j, e in enumerate(abs(c_right_diff)) if e > 2]
    index = list(set().union(i, j))
    
    for i in index:
      c_left_diff[i] = 0
      c_right_diff[i] = 0
    
    for i in range(len(c_left_diff)):
        if i == 0:
            continue
        
        alfa = atan2(c_left_diff[i]-c_right_diff[i], 2*wdt/dpp)
        heading.append(heading[-1] - 2*alfa)

        d = dpp/2 * (c_left_diff[i] + c_right_diff[i])

        x += d*cos(heading[-1])
        y += d*sin(heading[-1])
        camx.append(x + campos*cos(heading[-1]))
        camy.append(y + campos*sin(heading[-1]))
        lx.append(x)
        ly.append(y)
        
    
    return camx, camy, heading

#c_left = [i for i in range(110)]
#c_right = [0 for i in range(110)]

#wo_location(c_left, c_right, 'lol')
