import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
#import utm
import math
import glob
import os
from sensor_location import *



list_of_files_t265 = sorted(glob.glob('test/t265/calib*'))



for counter, t265_file in enumerate(list_of_files_t265):
   
    t = []
    v_l = []
    v_lx = []
    v_ly = []
    v_r = []
    v_rx = []
    v_ry = []
    v_filt = []
    v_filt_old = 0
    t_old = 0
    T = 1/4
    v_filt_list = []
    
    first = True
   


    with open(t265_file, 'r') as f:
        for line in f:
        
        # print(line.split(' ')[0])
            x = line.split(' ')[3]
            z = line.split(' ')[5]
            
            if first:
            
                first = False
                t_first = float(line.split(' ')[1]) 
            
            
            t.append(float(line.split(' ')[1]) - t_first)
            
            t_now = float(line.split(' ')[1]) - t_first
            delta_t = (t_now - t_old) / 1000
            t_old = t_now

            
            
            #höger hjulhastighet
            v_x = float(line.split()[22].strip(","))
            v_y = float(line.split()[23].strip(","))
            v_z = float(line.split()[24].strip(","))
            
            v_rx.append(v_x)
            v_ry.append(v_z)
            v_r.append(math.sqrt(v_x**2+v_y**2+v_z**2))
            
            
           
            #vänster hjulhastighet
            
            v_x = float(line.split()[11].strip(","))
            v_y = float(line.split()[12].strip(","))
            v_z = float(line.split()[13].strip(","))
            
            v_lx.append(v_x)
            v_ly.append(v_z)
            v_l.append(math.sqrt(v_x**2+v_y**2+v_z**2))
            v_left = math.sqrt(v_x**2+v_y**2+v_z**2)
            v_filt = ( v_left * delta_t + v_filt_old * T ) / (delta_t + T)
            v_filt_old = v_filt
            v_filt_list.append(v_filt)


    v_l = np.array(v_l)
    
    var_left = np.var(v_l)
   


    v_r = np.array(v_r)
    
    var_right = np.var(v_r)
    
    
    fig2 = plt.figure()
    plt.plot(t, v_l, label='v_l')
    plt.plot(t, v_r, label='v_r')
    plt.plot(t,v_filt_list, label="v filt left")
    
    
    plt.legend()
 
    plt.title('Hjulhastighet from test: ' + t265_file)
    plt.xlabel('s')
    plt.ylabel('m/s')
    plt.show()
    #plt.savefig("")
    plt.close(fig2)
