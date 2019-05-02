from math import acos, asin, cos, sin, sqrt, atan2
from matplotlib import pyplot as plt
import numpy as np
from array_smooth import array_smoothing

def wo_location(c_left, c_right, filename):
    dpp = 0.55*3.14/29
    wdt = 1.08
    campos = 0.9
    ad = dpp/wdt
   
    heading = [3.14/2] #north
    location = [0, 0] # x, y
    x = 0
    y = -0.9
    lx= [0] 
    ly = [-0.9]
    camx = [0]
    camy = [0]

    c_left_diff = array_smoothing(c_left)
    c_right_diff = array_smoothing(c_right)

    c_left_diff_temp = c_left_diff[abs(c_left_diff) < 2]
    c_right_diff = c_right_diff[abs(c_left_diff) < 2]

    c_left_diff = c_left_diff_temp[abs(c_right_diff) < 2]
    c_right_diff = c_right_diff[abs(c_right_diff) < 2]
    
    for i in range(len(c_left_diff)):
        if i == 0:
            continue
        
        alfa = atan2(c_left_diff[i]-c_right_diff[i], 2*wdt/dpp)
        heading.append(heading[-1] - 2*alfa)
        

        #d1 = wdt/2 - cos(alfa)*wdt/2
        #d2 = sin(alfa)*wdt/2
        #d = sqrt(d1*d1 + d2*d2)
        
        d = dpp/2 * (c_left_diff[i] + c_right_diff[i])

        x += d*cos(heading[-1])
        y += d*sin(heading[-1])
        camx.append(x + campos*cos(heading[-1]))
        camy.append(y + campos*sin(heading[-1]))
        lx.append(x)
        ly.append(y)
        #print( x, y)
    
    #print([lx, ly])
    #plt.plot(lx, ly)
    #plt.plot(camx, camy)
    #plt.grid()
    #plt.axis('equal')
    #plt.title(filename)
    #plt.show()
    return camx, camy

#c_left = [i for i in range(110)]
#c_right = [0 for i in range(110)]

#wo_location(c_left, c_right, 'lol')