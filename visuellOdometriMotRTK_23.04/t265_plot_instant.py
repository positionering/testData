import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import utm
import math
import glob
import os
from sensor_location_smooth import wo_location
from path_from_wheel_speed import path_from_wheel_speed




list_of_files_t265 = sorted(glob.glob('test/t265/*'))
list_of_files_cords = sorted(glob.glob('test/cord/*'))


filelist = ['test/cord/test18.log', 'test/t265/test18_1.log', 'test/heading/test6U.log']

filename_T265 = max(list_of_files_t265, key=os.path.getctime)



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
cam_heading = [] 
            

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

      #T265 speed

      v_T265_x.append(float(line.split()[16].strip(",")))
      v_T265_z.append(float(line.split()[18]))
          

      #pulser
      tic_r.append(float(line.split()[20]))
      tic_l.append(float(line.split()[19]))

      x_T265.append(-float(x))
      z_T265.append(float(z))

      #heading
      cam_heading.append(-(float(line.split()[7])-3.141592))


    
    offset_x = x_gnss[0]
    offset_z = z_gnss[0]
    x_gnss = np.array(x_gnss)
    z_gnss = np.array(z_gnss)

    x_gnss = x_gnss - offset_x
    z_gnss = z_gnss - offset_z

    plt.plot(x_gnss, z_gnss, label='Route from RTK')

    wo_x, wo_y, wo_heading = wo_location(tic_l, tic_r, ' ')
    
    x_T265 = np.array(x_T265)
    z_T265 = np.array(z_T265)
    
    # Plottar t265 path
    fig = plt.figure()
    plt.plot(x_T265, z_T265, label='Route from T265')
    plt.plot(wo_x, wo_y, label='Route from wheel odometry')
    
    plt.legend()
    plt.axis('equal')
    plt.title('Observed data from test: ' + filename_T265)
    plt.xlabel('m')
    plt.ylabel('m')
    plt.show()
    plt.close(fig)

    # Plot heading mot tid
    fig2 = plt.figure()
    plt.plot(t[1:], wo_heading, label='wheel odometry heading')
    plt.plot(t, cam_heading, label='camera heading')
    plt.legend()

   # plt.savefig("figs/"+filename_T265.split("/")[2]+".png")
    plt.show()
    plt.close(fig2)

    lp = path_from_wheel_speed(np.array([v_lx,v_ly]).T,np.array(t),start=np.array([-0.54,0]))
    rp = path_from_wheel_speed(np.array([v_rx,v_ry]).T,np.array(t),start=np.array([0.54,0]))
        
    # Plottar wheel speed path
    fig3 = plt.figure()
    plt.plot(lp[:,0],lp[:,1], label='Route from left wheel speed')
    plt.plot(rp[:,0],rp[:,1], label='Route from right wheel speed')
    
    plt.legend()
    plt.axis('equal')
    plt.title('Observed data from test: ' + filename_T265)
    plt.xlabel('m')
    plt.ylabel('m')
    plt.show()
    plt.close(fig3)
    
    #plottar pluserna
    """
    fig4 = plt.figure()
    plt.plot(t, tic_r, label='tic_r')
    plt.plot(t, tic_l, label='tic_l')

    
    plt.legend()
 
    plt.title('Pulser from test: ' + t265_file)
    plt.xlabel('s')
    plt.ylabel('m/s')

    plt.savefig("figs/"+"Pulser "+t265_file.split("/")[2]+".png")
    plt.close(fig4)
    """
    

    
    

