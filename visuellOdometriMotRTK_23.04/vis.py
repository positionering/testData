import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os





list_of_files_t265 = sorted(glob.glob('test/t265/inomhus*'))
list_of_files_cords = sorted(glob.glob('test/cord/inomhus*'))



filelist = ['test/cord/test18.log', 'test/t265/test18_1.log', 'test/heading/test6U.log']

filename_T265 = max(list_of_files_t265, key=os.path.getctime)
filename_RTK = max(list_of_files_cords, key=os.path.getctime)


#filename_RTK = filelist[0] 
#filename_T265 = filelist[1]

#filename_head = filelist[2]

for counter, t265_file in enumerate(list_of_files_t265):
    #cords_file = list_of_files_cords[counter]
    #print(cords_file)
    print(t265_file)
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
    """
    with open(cords_file, 'r') as f:
        f = f.readlines()
       # del f[-1]
        for line in f:
            lat = line.split(' ')[3]
            lon = line.split(' ')[5]
            #tid, lat, lon = line.split(' ')
            u = utm.from_latlon(float(lat), float(lon))

            x_gnss.append(u[0])
            z_gnss.append(u[1])
    """
    with open(t265_file, 'r') as f:
        for line in f:
          # print(line.split(' ')[0])
            x = line.split(' ')[3]
            z = line.split(' ')[5]
            
            if first:
            
                first = False
                t_first = float(line.split(' ')[1]) 
            
            
            t.append(float(line.split(' ')[1]) - t_first)
            
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
            
            #pulser
            tic_r.append(float(line.split()[20]))
            tic_l.append(float(line.split()[19]))
            
            x_T265.append(-float(x))
            z_T265.append(float(z))


    #offset_x = x_gnss[0]
    #offset_z = z_gnss[0]
    #x_gnss = np.array(x_gnss)
    #z_gnss = np.array(z_gnss)

    #x_gnss = x_gnss - offset_x
    #z_gnss = z_gnss - offset_z

    x_T265 = np.array(x_T265)
    z_T265 = np.array(z_T265)
    fig = plt.figure()
    plt.plot(x_T265, z_T265, label='Route from T265')
    #plt.plot(x_gnss, z_gnss, label='Route from RTK')

    plt.legend()
    plt.axis('equal')
    plt.title('Observed data from test: ' + t265_file)
    plt.xlabel('m')
    plt.ylabel('m')

    plt.savefig("figs/"+t265_file.split("/")[2]+".png")
    plt.close(fig)
    
    #plottar hjulhastigheten
    fig2 = plt.figure()
    plt.plot(t, v_l, label='v_l')
    plt.plot(t, v_r, label='v_r')
    
    plt.legend()
 
    plt.title('Hjulhastighet from test: ' + t265_file)
    plt.xlabel('s')
    plt.ylabel('m/s')

    plt.savefig("figs/"+"hjulhastighet "+t265_file.split("/")[2]+".png")
    plt.close(fig2)
    
    # Plott hjulhastigheter i 3D
    mpl.rcParams['legend.fontsize'] = 10
    
    fig3D = plt.figure()
    ax = fig3D.gca(projection='3d')
    
    v_l3D = np.array([v_lx,v_ly,t])
    v_l3D = v_l3D.T
    v_r3D = np.array([v_rx,v_ry,t])
    v_r3D = v_r3D.T
   
    ax.plot(v_l3D[:,0],v_l3D[:,1],v_l3D[:,2], label='v_l')
    ax.plot(v_r3D[:,0],v_r3D[:,1],v_r3D[:,2], label='v_r')
    
    plt.title('3D-Hjulhastighet from test: ' + t265_file)
    #ax.xlabel('m/s')
    #ax.ylabel('m/s')
    #ax.zlabel('ms')
    
    ax.legend()
    
    #plt.show()

    plt.savefig("figs/"+"3d-hjulhastighet "+t265_file.split("/")[2]+".png")
    plt.close(fig3D)
    
    
    #plottar pluserna
    fig3 = plt.figure()
    plt.plot(t, tic_r, label='tic_r')
    plt.plot(t, tic_l, label='tic_l')

    
    plt.legend()
 
    plt.title('Pulser from test: ' + t265_file)
    plt.xlabel('s')
    plt.ylabel('m/s')

    plt.savefig("figs/"+"Pulser "+t265_file.split("/")[2]+".png")
    plt.close(fig3)
    


#def dotproduct(v1, v2):
#    return sum((a*b) for a, b in zip(v1, v2))


#def length(v):
#    return math.sqrt(dotproduct(v, v))


#def angle(v1, v2):
#    return math.acos(dotproduct(v1, v2) / length(v1) * length(v2))

#reference_angle = angle(z_temp_RTK, z_temp_T265)

#reference_angle = math.atan2(z_T265[index_T265] - z_gnss[index_RTK], x_T265[index_T265] - x_gnss[index_RTK])
#print(reference_angle)
#print(z_T265[index_T265])
#print(z_gnss[index_RTK])


#x_T265 = np.cos(reference_angle)*x_T265 - np.sin(reference_angle)*z_T265
#z_T265 = np.sin(reference_angle)*x_T265 + np.cos(reference_angle)*z_T265


