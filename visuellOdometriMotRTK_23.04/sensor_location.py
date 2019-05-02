from math import acos, asin, cos, sin, sqrt
from matplotlib import pyplot as plt

def wo_location(c_left, c_right, filename):
    dpp = 0.55*3.14/29
    wdt = 1.08
    campos = 0.9
    ad = dpp/wdt
    d1 = wdt/2 - cos(ad)*wdt/2
    d2 = sin(ad)*wdt/2
    d = sqrt(d1*d1 + d2*d2)
    heading = [3.14/2] #north
    location = [0, 0] # x, y
    x = 0
    y = -0.9
    lx= [0] 
    ly = [-0.9]
    camx = [0]
    camy = [0]


    for i in range(len(c_left)):
        if i == 0:
            continue
        
        if c_left[i]-c_left[i-1] != 0 and c_right[i]-c_right[i-1] != 0:
            x += dpp*cos(heading[-1])
            y += dpp*sin(heading[-1])
            lx.append(x)
            ly.append(y)
            continue

        elif c_left[i]-c_left[i-1] != 0:
            heading.append(heading[-1] - ad)
            

        elif c_right[i]-c_right[i-1] != 0:
            heading.append(heading[-1] + ad)
        else:
            continue
        
        x += d*cos(heading[-1])
        y += d*sin(heading[-1])
        camx.append(x + campos*cos(heading[-1]))
        camy.append(y + campos*sin(heading[-1]))
        lx.append(x)
        ly.append(y)    
        print(heading, x, y)

    plt.plot(lx, ly)
    plt.plot(camx, camy)
    plt.grid()
    plt.axis('equal')
    plt.title(filename)
    plt.show()

c_left = [i for i in range(110)]
c_right = [0 for i in range(110)]

wo_location(c_left, c_right, 'lol')