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
from scipy.integrate import cumtrapz




t265_list_of_files = sorted(glob.glob('test/t265/190508*')) 
gnss222_list_of_files = sorted(glob.glob('test/cord222/190508*'))
gnss223_list_of_files = sorted(glob.glob('test/cord223/190508*'))


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
            t_temp = float(line.split()[1])
            if t_temp in t_t265:
                continue
            t_t265.append(t_temp)

            
            # t265
            t265_pos_x.append(float(line.split()[3]))
            t265_pos_z.append(-float(line.split()[5])) #speglar runt x
            
            #tic
            tic_r.append(float(line.split()[20]))
            tic_l.append(float(line.split()[19]))

    # Delete first to fit wo
    del t265_pos_x[0]
    del t_t265[0]
    del t265_pos_z[0]
    
    # Wheel odometry position
    wo_pos_x, wo_pos_z, wo_heading_rad = wo_location(tic_l, tic_r, "filename")

    wo_pos = fix_data(np.array([wo_pos_x,wo_pos_z]).T,1)
    wo_pos_x = wo_pos[:,0]
    wo_pos_z = wo_pos[:,1]

    # t265 position
    t265_pos = fix_data(np.array([t265_pos_x,t265_pos_z]).T,1)
    t265_pos_x = t265_pos[:,0]
    t265_pos_z = t265_pos[:,1]

    # Time adjust
    t_t265 = np.array([t_t265]).T
 
    np.apply_along_axis(int32,1,t_t265)

    t_222 = np.array(t_222).T 
    t_223 = np.array(t_223).T 

    sub = min(t_223[0],t_222[0],t_t265[0])        
    t_t265 -= sub
    t_222 -= sub
    t_223  -= sub
        
    start = int(max(t_223[0],t_222[0],t_t265[0][0]))
    end = int(min(t_223[-1],t_222[-1],t_t265[-1]))
    
    time = np.arange(start,end,50)

    t_t265 = np.array(t_t265).squeeze()
    t_222 = np.array(t_222).squeeze()
    t_223 = np.array(t_223).squeeze()
    # GNSSdata
    

    gnss222_pos_x = np.array(gnss222_pos_x)
    gnss222_pos_z = np.array(gnss222_pos_z)
    gnss223_pos_x = np.array(gnss223_pos_x)
    gnss223_pos_z = np.array(gnss223_pos_z)



    # Interpolate 
    f_interp_222_x = interp1d(t_222, gnss222_pos_x, kind="cubic" )
    f_interp_222_z = interp1d(t_222, gnss222_pos_z, kind="cubic")
    
    f_interp_223_x = interp1d(t_223, gnss223_pos_x, kind="cubic")
    f_interp_223_z = interp1d(t_223, gnss223_pos_z, kind="cubic")
    
    
    f_interp_t265_x = interp1d(t_t265, t265_pos_x, kind="cubic")
    f_interp_t265_z = interp1d(t_t265, t265_pos_z, kind="cubic")


    f_interp_wo_x = interp1d(t_t265, wo_pos_x, kind="cubic")
    f_interp_wo_z = interp1d(t_t265, wo_pos_z, kind="cubic")

    
    f_interp_222_x_value = f_interp_222_x(time)
    f_interp_222_z_value = f_interp_222_z(time)
    f_interp_223_x_value = f_interp_223_x(time)
    f_interp_223_z_value = f_interp_223_z(time)
    f_interp_t265_x_value = f_interp_t265_x(time)
    f_interp_t265_z_value = f_interp_t265_z(time)
    f_interp_wo_x_value = f_interp_wo_x(time)
    f_interp_wo_z_value = f_interp_wo_z(time)

    t265_pos = np.array([f_interp_t265_x_value ,f_interp_t265_z_value])
    
    # Fix GNSS date, angle + center
    gnss_data = fix_GPSdata(np.array([f_interp_223_x_value,f_interp_223_z_value]).T, np.array([f_interp_222_x_value,f_interp_222_z_value]).T, 1, 2).T

    # GNSS traveled length
    gnss_len = np.sqrt( np.square(gnss_data[0]) + np.square(gnss_data[1]) )
    
    # Error
    t265_error = np.sqrt( (gnss_data[0] - t265_pos[0,:] )**2 + (gnss_data[1] - t265_pos[1,:] )**2 )
    wo_error = np.sqrt( (gnss_data[0] - f_interp_wo_x_value )**2 + (gnss_data[1] - f_interp_wo_z_value )**2 )
    gnss_error = abs(np.sqrt( (f_interp_222_x_value - f_interp_223_x_value )**2 + (f_interp_222_z_value - f_interp_223_z_value )**2 ) -0.71 ) /2 

    # CUM ERROR
    wo_cum = cumtrapz(wo_error, time)
    t265_cum = cumtrapz(t265_error, time)
    gnss_cum = cumtrapz(gnss_error, time)
    
    # Plot
    fig = plt.figure()

    plt.subplot(2, 2, 1)
    plt.plot(t265_pos[0,:], t265_pos[1,:], label="Visuell odometri")
    plt.plot(gnss_data[0], gnss_data[1], label="GNSS")
    plt.plot(f_interp_wo_x_value,f_interp_wo_z_value, label="Hjulodometri")
    plt.axis('equal')
    plt.title('Uppmätt körbana')
    plt.xlabel("Sträcka [m]")
    plt.ylabel("Sträcka [m]")
    plt.legend()
    
    plt.subplot(2, 2, 2)
    #konverterar till sekunder
    plt.plot(time/1000,t265_error, label="Visuell odometri")
    plt.plot(time/1000, gnss_error, label="GNSS")
    plt.plot(time/1000,wo_error, label="Hjulodometri")
    plt.title('Beräknat fel över tid')
    plt.xlabel("Tid [s]")
    plt.ylabel("Sträcka [m]")
    plt.legend()

    plt.subplot(2,2,3)
    plt.plot(gnss_len, t265_error, label="Visuell odometri")
    plt.plot(gnss_len, gnss_error, label="GNSS")
    plt.plot(gnss_len, wo_error, label="Hjulodometri")
    plt.title('Beräknat fel över körsträcka')
    plt.xlabel("Sträcka [m]")
    plt.ylabel("Fel integretat över tid")
    plt.legend()


    plt.subplot(2,2,4)
    #konverterar till sekunder
    plt.plot(time[:-1]/1000, t265_cum/1000, label="Visuell odometri")
    plt.plot(time[:-1]/1000, gnss_cum/1000, label="GNSS")
    plt.plot(time[:-1]/1000, wo_cum/1000, label="Hjulodometri")
    plt.title('Integrerat fel')
    plt.xlabel("Tid [s]")
    plt.ylabel("Fel integretat över tid")
    plt.legend()
    
    plt.show()
    


    # Tabel
    celltext= [['{}'.format(t265_error[-1]), '{}'.format(wo_error[-1]), '{}'.format(gnss_error[-1])],
    ['{}'.format(t265_cum[-1]), '{}'.format(wo_cum[-1]), '{}'.format(gnss_cum[-1])]]
    rows = ('Fel', 'Integrerat fel')
    columns = ('Visuell Odometri', 'Hjulodometri', 'GNSS' )
    plt.table(cellText=celltext,rowLabels=rows, colLabels=columns)

    plt.show()
    
    









