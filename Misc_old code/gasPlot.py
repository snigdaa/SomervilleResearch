import numpy as np
import os
import cStringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#haloTable = np.loadtxt('haloTable88.txt',dtype=str,delimiter=' ',skiprows=2,usecols=(4,7,9))
#print haloTable
#converters={3: (string.strip("'")), 6: (string.strip("'")), 8: (string.strip("'"))})

with open('haloTable88.txt','r') as myfile:
    data = myfile.read().replace("'","").replace("]","")
haloTable=np.loadtxt(cStringIO.StringIO(data),skiprows=2,usecols=(3,6,8))
print haloTable
gasMass = []
fsps_pdsize = []
#0th column: M_gas
#1st column: fsps size
#2nd column: pd size
for idx, val in enumerate(haloTable[:,1]):
    if haloTable[idx,1]!=100:
        insertVal = haloTable[idx,1]/haloTable[idx,2]
        if insertVal > 0:
            #fsps_pdsize.append(-1)
            fsps_pdsize.append(insertVal)
            gasMass.append(haloTable[idx,0])
print fsps_pdsize
y_axis = gasMass
x_axis = fsps_pdsize
print x_axis, y_axis

fig, ax = plt.subplots(figsize=(6,6),nrows=1,ncols=1)
fig.subplots_adjust(left=0.15,right=0.98,bottom=0.1,top=0.9)
ax.scatter(x_axis,y_axis,color='g',label='Gas Mass vs. FSPS/PD size ratio',marker='o')
#ax.plot(np.linspace(0,20),np.linspace(0,20),color='b',linestyle='dashed',label='1:1 ratio')
ax.set_xlabel('FSPS Half-light R/PD Half-light R',fontsize=18)
ax.set_ylabel('Gas Mass ($M_{sol}$)',fontsize=18)
#ax.set_xlim(0,20)
#ax.set_ylim(-1,1)
ax.legend()

fig.suptitle('Gas Mass vs. FSPS/PD size ratio, z=0',fontsize=20)
fig.savefig('/home/sss274/Work/images/gasVsSizeratio88.png')

#fig.suptitle('Gas Mass vs. FSPS/PD size ratio, z=1',fontsize=20)
#fig.savefig('/home/sss274/Work/images/gasVsSizeratio44.png')


