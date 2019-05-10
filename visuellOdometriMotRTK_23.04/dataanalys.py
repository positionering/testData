import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os
from sensor_location_smooth import array_smoothing, wo_location
from rotate_data import fix_GPSdata, center_data, rotate_data

# Filenames 
list_of_files_t265 = sorted(glob.glob('test/t265/*')) # TODO: Mappstruktur, filnamn
list_of_files_gnss_l = sorted(glob.glob('test/cord222/*'))
list_of_files_gnss_r = sorted(glob.glob('test/cord223/*'))

for t265_file, gnss_file_l, gnss_file_r in t265_list_of_files, gnss_list_of_files_l, gnss_list_of_files_r:
    

    ### PREDEF ###
    
    # Time
    t = np.array()

    # GNSSdata
    gnss_pos_x_r = np.array()
    gnss_pos_z_r = np.array()
    
    gnss_pos_x_l = np.array()
    gnss_pos_z_l = np.array()

    # Camera data
    t265_pos_x = np.array()
    t265_pos_z = np.array()

    t265_v_x = np.array()
    t265_v_z = np.array()

    # Wheel odometry data
    wo_tic_r = np.array()
    wo_tic_l = np.array()

    wo_v_r_x = np.array()
    wo_v_r_y = np.array()
    wo_v_r_z = np.array()


    wo_v_l_x = np.array()
    wo_v_l_y = np.array()
    wo_v_l_z = np.array()



    ### RETRIEVE DATA ###

    # From left gnss 
    with open(gnss_file_l, 'r') as f:
        for line in f:
            lat_l = line.split(' ')[3]
            lon_l = line.splot(' ')[5]
            u = utm.from_latlong(float(lat_l), float(lon_l))
            gnss_pos_x_l.append(u[0])
            gnss_pos_z_l.append(u[1])
    
    # From right gnss
    with open(gnss_file_r, 'r') as f:
        for line in f:
            lat_r = line.split(' ')[3]
            lon_r = line.splot(' ')[5]
            u = utm.from_latlong(float(lat_r), float(lon_r))
            gnss_pos_x_r.append(u[0])
            gnss_pos_z_r.append(u[1])

    # From t265, wheel odometry
    with open(t265_file, 'r') as f:
        for line in f:
            
            # time
            t.append(float(line.split()[1]))

            # t265, TODO: Datastruktur
            t265_pos_x.append(float(line.split()[3]))
            t265_pos_z.append(float(line.split()[5]))
            t265_v_x.append(float(line.split([18])))
            t265_v_z.append(float(line.split()[16]))

            # wheel odometry, TODO:
            wo_tic_l.append(float(line.split([19])))
            wo_tic_r.append(float(line.split()[20]))

            wo_v_l_x.append(float(line.split()[11]))
            wo_v_l_y.append(float(line.split()[12]))
            wo_v_l_z.append(float(line.split()[13]))

            wo_v_r_x.append(float(line.split()[22]))
            wo_v_r_y.append(float(line.split()[23]))
            wo_v_r_z.append(float(line.split()[24]))
    

    ### Data calculations ###

    # Time adjust
    t -= t[0]

    # Calculate path from wo-tics
    wo_pos_x, wo_pos_y = wo_location(wo_tic_l, wo_tic_r, ' ')gnss_pos_x, gnss_pos_z,

    # Defining the origo for gnss values
    gnss_pos = fix_GPSdata(np.array([gnss_pos_x_l, gnss_pos_y_h]), np.array([gnss_pos_x_r, gnss_pos_y_r]))


    ### PLOTTING ###

    # Plot 1: POS GNSS och hjulodometri
    fig = plt.figure()

    plt.plot(gnss_pos_x, gnss_pos_z, label='Rutt från RTK-GNSS')
    plt.plot(wo_pos_x, wo_pos_z, label='Rutt från hjulodometri')
    
    plt.title('Position enligt GNSS och hjulodometri från test:' + t265_file) # TODO: Mappstruktur, filnamn
    plt.xlabel('Position [m]')
    plt.ylabel('Position [m]')
    plt.axis('equal')
    plt.legend()
    plt.grid()
    
    plt.savefig('sluttest/figures/' + t265_file.split('/')[2].split('.')[0] + 'POS:GNSS_WO.png') # TODO: Mappstruktur
    plt.close(fig)

    # Plot 2: POS GNSS och T265
    fig2 = plt.figure()

    plt.plot(gnss_pos_x, gnss_pos_z, label='Rutt från RTK-GNSS')
    plt.plot(t265_pos_x, t265_pos_z, label='Rutt från T265')
    
    plt.title('Position enligt GNSS och T265 från test:' + t265_file)
    plt.xlabel('Position [m]')
    plt.ylabel('Position [m]')
    
    plt.axis('equal')
    plt.legend()
    plt.grid()
    
    plt.savefig('sluttest/figures/' + t265_file.split('/')[2].split('.')[0] + 'POS:GNSS_T265.png') # TODO: Mappstruktur
    plt.close(fig2)

    # Plot 3: VEL Hjulhastighet mot tid
    fig3 = plt.figure()

    plt.plot(t, wo_v_l, label='Vänster hjul')
    plt.plot(t, wo_v_r, label='Höger hjul')
    
    plt.title('Hastighet enligt hjulodometri från test:' + t265_file)
    plt.xlabel('Tid [ms]')
    plt.ylabel('Hastighet [m/s]')
    
    plt.legend()
    
    plt.savefig('sluttest/figures/' + t265_file.split('/')[2].split('.')[0] + '_VEL:WO.png') # TODO: Mappstruktur
    plt.close(fig3)


