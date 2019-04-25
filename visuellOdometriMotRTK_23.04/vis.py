import numpy as np
from scipy.integrate import simps
from scipy.integrate import cumtrapz
from numpy import trapz
import matplotlib.pyplot as plt
import utm

x_gnss = []
z_gnss = []
x_T265 = []
z_T265 = []


filelist = ['test/t265/test4U_0.log', 'test/cord/test1.log']
filename = filelist[0]

if filename == filelist[1]:
    with open(filename, 'r') as f:
        for line in f:
            lat, lon = line.split(' ')
            u = utm.from_latlon(float(lat), float(lon))

            x_gnss.append(u[0])
            z_gnss.append(u[1])

elif filename == filelist[0]:
    with open(filename, 'r') as f:
        for line in f:
            x = line.split(' ')[0]
            z = line.split(' ')[2]
            x_T265.append(float(x))
            z_T265.append(float(z))

print(len(x_T265))
#offset_x = x_gnss[0]
#offset_z = z_gnss[0]
#x_gnss = np.array(x_gnss)
#z_gnss = np.array(z_gnss)

#x_gnss = x_gnss - offset_x
#z_gnss = z_gnss - offset_z

x_T265 = np.array(x_T265)
z_T265 = np.array(z_T265)

plt.plot(x_T265, z_T265)
#plt.plot(x_gnss, z_gnss)
plt.show()