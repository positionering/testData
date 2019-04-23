from __future__ import print_function

import numpy as np
from scipy.integrate import simps
from scipy.integrate import cumtrapz
from numpy import trapz
import matplotlib.pyplot as plt



nr = 3


nm  = ['testlogs/wodometry_test_first30',
        'testlogs/wodometry_test_second30',
        'testlogs/wodometry_test_third30slow',
        'testlogs/wodometry_test_fourth30slowfast',
        'testlogs/wodometry_test_fifth30fast',
        'testlogs/wodometry_test_sixth90normal']

distances = [60, 30, 30, 30, 30, 90]


f=open(nm[nr-1],"r")
lines=f.read().splitlines() 
tid=[]
wh1=[]
wh2=[]

interval = 0
d = 0.00
for x in lines:
    n = float((x.split(' ')[4]).split(':')[1])
    t1 = float((x.split(' ')[2]).split(':')[1])
    t2 = float((x.split(' ')[3]).split(':')[1])
    w1 = float((x.split(' ')[0]).split(':')[1])
    w2 = float((x.split(' ')[1]).split(':')[1])
    if n - d > interval:
        tid.append(n*1e-3)
        wh1.append(w1/3.6)
        wh2.append(w2/3.6)
        ntick1 = float((x.split(' ')[2]).split(':')[1])
        ntick2 = float((x.split(' ')[3]).split(':')[1])
    d = n
f.close()

# Adjust the wheel diameter
meand1 = np.mean(np.array([0.544, 0.545, 0.545, 0.546, 0.554, 0.545]))
meand2 = np.mean(np.array([0.544, 0.546, 0.546, 0.545, 0.545, 0.545]))

wh1a = [x/0.55 * meand1 for x in wh1]
wh2a = [x/ 0.55 * meand2 for x in wh2]

#numpys trapz
dist_trapz1 = trapz(wh1a,tid)
dist_trapz2 = trapz(wh2a,tid)
print("distance trapz integral wh1 =", dist_trapz1)
print("distance trapz integral wh2 =", dist_trapz2)

#scipys trapz
dist_cumtrapz1 = cumtrapz(wh1a, tid, initial=0)
dist_cumtrapz2 = cumtrapz(wh2a, tid, initial=0)
print("distance cumtrapz integral wh1 =", dist_cumtrapz1[-1])
print("distance cumtrapz integral wh2 =", dist_cumtrapz2[-1])

#scipys simps
dist_simps1 = simps(wh1a, tid)
dist_simps2 = simps(wh2a, tid)
print("distance simps integral wh1 =", dist_simps1)
print("distance simps integral wh2 =", dist_simps2)

#Tickräkning
print('TICK1:', ntick1)
print('TICK2:', ntick2)
#whd1 = 90/ntick1/3.14159265*29
#whd2 = 90/ntick2/3.14159265*29
#print('Calc whd1:', whd1 , ' whd2:', whd2)

#Plotting
fig, (ax1, ax2) = plt.subplots(2,1)
fig.suptitle('Test nummer ' + str(nr), fontweight='bold')


fig.subplots_adjust(hspace=0.7)


ax1.plot(tid, wh1, 'r--', tid, wh2, 'b--')
ax1.set_xlabel('Tid [s]')
ax1.set_ylabel('Hastighet [m/s]')
ax1.set_title('Hastighet över tid')
ax1.legend(['Vänster Hjul', 'Höger Hjul'])
ax1.grid()

ax2.plot(tid, dist_cumtrapz1, 'r--', tid, dist_cumtrapz2, 'b--')
ax2.set_xlabel('Tid [s]')
ax2.set_ylabel('Distans [m]')
ax2.set_title('Distans över tid')
ax2.legend(['Vänster Hjul', 'Höger Hjul'], loc='lower right')
ax2.grid()


#plt.subplot(2,1,1)
#plt.plot(tid, dist_cumtrapz1, 'r-', tid, dist_cumtrapz2, 'b-')
#set_xlabel('distance [m]')
#plt.plt.grid()
#plt.subplot(2,1,2)
#plt.plot(tid, wh1, 'g--', tid, wh2, 'r--')
#plt.grid()

plt.show()
