import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os
from sensor_location_smooth import *
from fix_data import *
from scipy.interpolate import interp1d
from scipy.integrate import trapz




t265_list_of_files = sorted(glob.glob('test/t265/190508rakF*')) 
gnss222_list_of_files = sorted(glob.glob('test/cord222/190508rakF*'))
gnss223_list_of_files = sorted(glob.glob('test/cord223/190508rakF*'))


for i,t265_file in enumerate(t265_list_of_files):

    gnss222_file = gnss222_list_of_files[i]
    gnss223_file = gnss223_list_of_files[i]


    ### PREDEF ###
    
    # Time
    t_t265 = []
    t_222 = []
    t_223 = []

    # GNSSdata
    gnss222_pos_x = []
    gnss222_pos_z = []
    gnss223_pos_x = []
    gnss223_pos_z = []

    # Camera data
    t265_pos_x = []
    t265_pos_z = []

    #Tic data
    tic_r = []
    tic_l = []
     ### RETRIEVE DATA ###

    # From gnss
    with open(gnss222_file, 'r') as f1:
        f1 = f1.readlines()
        del f1[-1]
        for line in f1:
            t_222.append(float(line.split()[1]))
            lat = line.split()[3]
            lon = line.split()[5]
            u = utm.from_latlon(float(lat), float(lon))
            gnss222_pos_x.append(u[0])
            gnss222_pos_z.append(u[1])

    with open(gnss223_file, 'r') as f2:
        f2 = f2.readlines()
        del f2[-1]
        for line in f2:
            t_223.append(float(line.split()[1]))
            lat = line.split()[3]
            lon = line.split()[5]
            u = utm.from_latlon(float(lat), float(lon))
            gnss223_pos_x.append(u[0])
            gnss223_pos_z.append(u[1])
    
    # From t265, wheel odometry
    with open(t265_file, 'r') as f3:
        for line in f3:
            
            # time
            t_t265.append(float(line.split()[1]))

            # t265
            t265_pos_x.append(float(line.split()[3]))
            t265_pos_z.append(-float(line.split()[5])) #speglar runt x
            
            #tic
            tic_r.append(float(line.split()[20]))
            tic_l.append(float(line.split()[19]))

    # Wheel odometry position
    
   
    wo_pos_x, wo_pos_z, wo_heading_rad = wo_location(tic_l, tic_r, "filename")

    wo_pos = np.array([wo_pos_x,wo_pos_z])

    #time
    t_t265 = np.array(t_t265).T
    t_222 = np.array(t_222).T
    t_223 = np.array(t_223).T

    t_222 = center_data(t_222)
    t_223 = center_data(t_223)
    t_t265 = center_data(t_t265)


    t_t265 = np.array(t_t265).squeeze()
    t_222 = np.array(t_222).squeeze()
    t_223 = np.array(t_223).squeeze()
    # GNSSdata
   
    

    gnss222_pos_x = np.array(gnss222_pos_x)
    gnss223_pos_z = np.array(gnss223_pos_z)

    
    # Camera data
    t265_pos = np.array([t265_pos_x,t265_pos_z]) #roterar 180



    #Calc

    #Calculate error:
    
    
    #GNS error
    try:
        gnss_error = abs(np.sqrt( (gnss222_pos_x - gnss223_pos_x )**2 + (gnss222_pos_z - gnss223_pos_z )**2 ) -0.71 )
    except:
        #print(t265_file)
        continue

    #Interpolate GNSS data
    f_interp_222_x = interp1d(t_222, gnss222_pos_x,fill_value="extrapolate")
    f_interp_222_z = interp1d(t_222, gnss222_pos_z,fill_value="extrapolate")
    
    f_interp_223_x = interp1d(t_223, gnss223_pos_x,fill_value="extrapolate")
    f_interp_223_z = interp1d(t_223, gnss223_pos_z,fill_value="extrapolate")

    t265_cum_error = []
    for T in range(0, 2000, 10):
        f_interp_222_x_value = f_interp_222_x(t_t265+T)
        f_interp_222_z_value = f_interp_222_z(t_t265+T)
        
        f_interp_223_x_value = f_interp_223_x(t_t265+T)
        f_interp_223_z_value = f_interp_223_z(t_t265+T)
        
        #Fix GNSS date, angle + center
        gnss_data = fix_GPSdata(np.array([f_interp_223_x_value,f_interp_223_z_value]).T, np.array([f_interp_222_x_value,f_interp_222_z_value]).T, 1, 2).T

        #t265 error
        t265_error = np.sqrt( (gnss_data[0] - t265_pos[0,:] )**2 + (gnss_data[1] - t265_pos[1,:] )**2 )
        t265_cum_error.append(np.array([T, trapz(t265_error, t_t265)]))
        
        #print(max(t265_error))
    
    t265_cum_error = np.array(t265_cum_error)
    delay = t265_cum_error[np.argmin(t265_cum_error[:,1]),0]
    #print('----------',delay)

    #Wheel odometry error
    #wo_error = 


        

    plt.plot(t265_pos[0,:], t265_pos[1,:],"b")
    
    plt.plot(gnss_data[0], gnss_data[1], "r" )
    plt.axis('equal')
    plt.show()

    plt.plot(t_t265,t265_error)
    plt.show()
    
    









