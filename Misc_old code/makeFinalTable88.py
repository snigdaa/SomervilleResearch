import os
from shutil import copyfile,move,copy
import numpy as np
from array import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

doneFiles = ['28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','48']
#4,8,10,17,18
errors = ['32','36','38','48']
unableorable = [0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1]            

tempIDArray = []

halodir = '/home/ec675/Work/pd'
for root,dirs,files in os.walk(halodir):
    for each in dirs:
        for nums in doneFiles:
            if nums==each[:2]:
                tempIDArray.append(each[:8])
index_array = np.argsort(tempIDArray)
IDArray = []
for each in index_array:
    IDArray.append(tempIDArray[each])

m200 = []
stellarmass = []
rad3D = []
faceonRadM = []
faceonRadL = []

finalhalfL = []

gas = []

rootdir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'
for root,dirs,files in os.walk(rootdir):
    for IDs in IDArray:
        for each in dirs:
            if each == IDs[3:]:
                tempdir = rootdir + each
                for one, two, three in os.walk(tempdir):
                    for each in three:
                        if each == 'info_088.txt':
                            info = open(tempdir+'/'+each)
                            for idx, line in enumerate(list(info)):
                                if idx==17:
                                    m200.append(line[21:33])
                                if idx==14:
                                    stellarmass.append(line[21:33])
                                if idx==18:
                                    gas.append(line[21:33])
                                if idx==24:
                                    rad3D.append(line[21:33])
                                if idx==25:
                                    if line[21:33] == 'None\n':
                                        faceonRadM.append(-1)
                                    else:
                                        faceonRadM.append(line[21:33])
                                if idx==26:
                                    if line[21:33] == 'None\n':
                                        faceonRadL.append(-1)
                                    else:
                                        faceonRadL.append(line[21:33])

smaArray = open('/home/sss274/Work/isophotelists/88halflightSMA.txt')
counter = 0
finalhalfL = smaArray.read().splitlines()

for idx, val in enumerate(doneFiles):
    if idx == 4 or idx == 8 or idx == 10 or idx == 17 or idx == 18:
        finalhalfL.insert(idx,-1)

smaArray.close()

final = np.dstack((IDArray,m200,stellarmass,gas,rad3D,faceonRadM,faceonRadL,unableorable,finalhalfL))

print faceonRadL
m200flt = np.zeros_like(m200)
stellarmassflt = np.zeros_like(stellarmass)
gasflt = np.zeros_like(gas)
rad3Dflt = np.zeros_like(rad3D)
faceonRadMflt = np.zeros_like(faceonRadM)
faceonRadLflt = np.zeros_like(faceonRadL)
finalhalfLflt = np.zeros_like(finalhalfL)
for idx, val in enumerate(m200):
    m200flt[idx] =float(m200[idx])
    stellarmassflt[idx] = float(stellarmass[idx])
    gasflt[idx] = float(gas[idx])
    rad3Dflt[idx] = float(rad3D[idx])
    faceonRadMflt[idx] = float(faceonRadM[idx])
    faceonRadLflt[idx] = float(faceonRadL[idx])
    finalhalfLflt[idx] = float(finalhalfL[idx])
#np.save('haloTable88', final)

fig, (ax1,ax2,ax3) = plt.subplots(figsize = (18,6), nrows=1, ncols=3)
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.9)
ax1.scatter(rad3Dflt,finalhalfLflt, color='g',marker='s')
ax2.scatter(faceonRadMflt,finalhalfLflt, color='g', marker='o')
ax3.scatter(rad3Dflt,finalhalfLflt, color='r',marker='s', label='3D model')
ax3.scatter(faceonRadMflt,finalhalfLflt, color='b',marker='o', label='Face-on Mass-weighted R')
ax1.set_xlabel('Half-mass R from 3D model ($kpc$)', fontsize = 18)
ax2.set_xlabel('Half-mass R from face-on projection M ($kpc$)', fontsize = 18)
ax3.set_xlabel('Half-mass R ($kpc$)', fontsize = 18)
ax1.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax2.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax3.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
fig.suptitle('Half-light R (PD) vs. FSPS Rads', fontsize=20)

ax1.set_xlim(0,20)
ax2.set_xlim(0,20)
ax3.set_xlim(0,20)
ax3.set_ylim(0,2.5)
ax2.set_ylim(0,1)
ax1.set_ylim(0,1)

ax3.plot(np.linspace(0,20),np.linspace(0,20),color='g',linestyle='dashed',linewidth=2,label='ideal relation')
ax3.legend(loc='upper right',bbox_to_anchor=(1,1))

fig.savefig('/home/sss274/Work/images/halfLRPDvsFSPSradsinfo44.png')

fig, ax = plt.subplots(figsize = (6,6), nrows=1, ncols=1)
fig.subplots_adjust(left=0.12, right=0.98, bottom=0.13, top=0.9)
ax.scatter(faceonRadLflt,finalhalfLflt, color='b',label='Half-light R (Powderday) vs. Half-light R (FSPS)',marker='o')
ax.set_xlabel('Half-light R (Powderday) ($kpc$)', fontsize = 18)
ax.set_ylabel('Half-light R (fsps) $(kpc)$', fontsize = 18)
#ax.set_xlim(0,6)
ax.set_ylim(0,10)

ax.plot(np.linspace(0,13),np.linspace(0,13),color='g', linestyle='dashed', linewidth=2,label=r'ideal relation $(f(x) = x)$')
#ax.plot(np.linspace(0,13),correction,color='r', linestyle='dashed', linewidth=2,label=r'correction factor$(f(x) = 0.15x)$')
ax.legend(loc='upper right',bbox_to_anchor=(1,1))

#fig.suptitle('Half-Mass R vs. Half-Light R', fontsize=20)
fig.suptitle('Calculated Half-L R vs. PD Half-L R', fontsize=20)
fig.savefig('/home/sss274/Work/images/HalfLightFSPSvPDinfo88.png')

