import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os
from sensor_location_smooth import *



t265_list_of_files = sorted(glob.glob('test/t265/test*')) 
gnss222_list_of_files = sorted(glob.glob('test/cord222/test*'))
gnss223_list_of_files = sorted(glob.glob('test/cord223/test*'))


print(t265_list_of_files)

print(gnss222_list_of_files)

print(gnss223_list_of_files)
for t265_file, gnss222_file, gnss223_file in t265_list_of_files, gnss222_list_of_files, gnss223_list_of_files:
    

    ### PREDEF ###
    
    # Time
    t = []

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
    with open(gnss222_file, 'r') as f:
        f = f.readlines()
        del f[-1]
        for line in f:
            lat = line.split()[3]
            lon = line.split()[5]
            u = utm.from_latlon(float(lat), float(lon))
            gnss222_pos_x.append(u[0])
            gnss222_pos_z.append(u[1])

    with open(gnss223_file, 'r') as f:
        f = f.readlines()
        del f[-1]
        for line in f:
            lat = line.split()[3]
            lon = line.split()[5]
            u = utm.from_latlon(float(lat), float(lon))
            gnss223_pos_x.append(u[0])
            gnss223_pos_z.append(u[1])
    
    # From t265, wheel odometry
    with open(t265_file, 'r') as f:
        for line in f:
            
            # time
            t.append(float(line.split()[1]))

            # t265
            t265_pos_x.append(float(line.split()[3]))
            t265_pos_z.append(float(line.split()[5]))
            
            #tic
            tic_r.append(float(line.split()[20]))
            tic_l.append(float(line.split()[19]))

    # Wheel odometry position
    wo_pos_x, wo_pos_z, wo_heading_rad = wo_location(tic_l, tic_r, "filename")

    wo_pos = np.array([wo_pos_x,wo_pos_z])

    #time
    t = np.array(t)

    # GNSSdata
    gnss222_pos = np.array([gnss222_pos_x,gnss222_pos_z])
    gnss223_pos = np.array([gnss223_pos_x,gnss223_pos_z])
    
    # Camera data
    t265_pos = np.array([t265_pos_x,t265_pos_z]).T

    print(t265_pos)
    print(type(t265_pos))
    # TODO: skicka in datan till funktion som roterar den, och justerar så att den börjar i noll


    #Calculate error:










