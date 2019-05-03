import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os
from sensor_location_smooth import *



list_of_files_t265 = sorted(glob.glob('test/t265/test18F*'))
list_of_files_cords = sorted(glob.glob('test/cord/test18F*'))



filelist = ['test/cord/test18.log', 'test/t265/test18_1.log', 'test/heading/test6U.log']

filename_T265 = max(list_of_files_t265, key=os.path.getctime)
filename_RTK = max(list_of_files_cords, key=os.path.getctime)


#filename_RTK = filelist[0] 
#filename_T265 = filelist[1]

#filename_head = filelist[2]

x_gnss = []
z_gnss = []
x_T265 = []
z_T265 = []
t = []
v_l = []
v_lx=[]
v_ly=[]
v_r = []
v_rx=[]
v_ry=[]
first = True
tic_r = []
tic_l = []
v_T265_x = []
v_T265_z = [] 
            

with open(filename_T265, 'r') as f:
    for line in f:
    # print(line.split(' ')[0])
        x = line.split(' ')[3]
        z = line.split(' ')[5]

        if first:

            first = False
            t_first = float(line.split(' ')[1]) 


        t.append(float(line.split(' ')[1]) - t_first)

        #höger hjulhastighet
        #v_x = float(line.split()[22].strip(","))
        #v_y = float(line.split()[23].strip(","))
        #v_z = float(line.split()[24].strip(","))

        #v_rx.append(v_x)
        #v_ry.append(v_z)
        #v_r.append(math.sqrt(v_x**2+v_y**2+v_z**2))


        #vänster hjulhastighet

        v_x = float(line.split()[11].strip(","))
        v_y = float(line.split()[12].strip(","))
        v_z = float(line.split()[13].strip(","))

        v_lx.append(v_x)
        v_ly.append(v_z)
        v_l.append(math.sqrt(v_x**2+v_y**2+v_z**2))

        #T265 speed

        v_T265_x.append(float(line.split()[16].strip(",")))
        v_T265_z.append(float(line.split()[18]))
            

        #pulser
        tic_r.append(float(line.split()[20]))
        tic_l.append(float(line.split()[19]))

        x_T265.append(-float(x))
        z_T265.append(float(z))


        offset_x = x_gnss[0]
        offset_z = z_gnss[0]
        x_gnss = np.array(x_gnss)
        z_gnss = np.array(z_gnss)

        x_gnss = x_gnss - offset_x
        z_gnss = z_gnss - offset_z

        camx, camy = wo_location(tic_l, tic_r, 'Hjuldata from test: ' + t265_file)

        x_T265 = np.array(x_T265)
        z_T265 = np.array(z_T265)
        
    # Plottar t265 path
    fig = plt.figure()
    plt.plot(x_T265, z_T265, label='Route from T265')
    plt.plot(x_gnss, z_gnss, label='Route from RTK')
    plt.plot(camx, camy, label='Route from wheel odometry')

    plt.legend()
    plt.axis('equal')
    plt.title('Observed data from test: ' + t265_file)
    plt.xlabel('m')
    plt.ylabel('m')

    plt.savefig("figs/"+t265_file.split("/")[2]+".png")
    plt.close(fig)
    
    #plottar pluserna
    """
    fig3 = plt.figure()
    plt.plot(t, tic_r, label='tic_r')
    plt.plot(t, tic_l, label='tic_l')

    
    plt.legend()
 
    plt.title('Pulser from test: ' + t265_file)
    plt.xlabel('s')
    plt.ylabel('m/s')

    plt.savefig("figs/"+"Pulser "+t265_file.split("/")[2]+".png")
    plt.close(fig3)
    """

    

    
    


