from math import acos, asin, cos, sin, sqrt
from matplotlib import pyplot as plt

def wo_location(c_left, c_right):
    dpp = 0.55*3.14/29
    wdt = 1.08
    ad = 2*3.14/29
    d1 = wdt/2 - cos(ad)*wdt/2
    d2 = sin(ad)*wdt/2
    d = sqrt(d1*d1 + d2*d2)
    heading = 3.14/2 #north
    location = [0, 0] # x, y
    x = 0
    y = 0
    lx= [0] 
    ly = [0]
    for i in range(len(c_left)):
        if i == 0:
            continue
        
        if c_left[i]-c_left[i-1] != 0 and c_right[i]-c_right[i-1] != 0:
            x += dpp*cos(heading)
            y += dpp*sin(heading)
            lx.append(x)
            ly.append(y)
            continue

        if c_left[i]-c_left[i-1] != 0:
            heading -= ad
            x += d*cos(heading)
            y += d*sin(heading)
            lx.append(x)
            ly.append(y)

        if c_right[i]-c_right[i-1] != 0:
            heading += ad

            x -= d*cos(heading)
            y += d*sin(heading)
        print(heading, x, y)

    plt.plot(lx, ly)
    plt.grid()
    plt.axis('equal')
    plt.show()