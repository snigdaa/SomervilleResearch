#THIS IS THE FINAL THING WE'LL USE TO MAKE THE TABLES
#THE HALFLIGHT ARRAY WILL BE MADE AS YOU USE PHOTUTILSISO.PY
z = "044"
cosmodir = "cosmo_nodust_44/"
npix = 512

import os
from shutil import copyfile,move,copy
import numpy as np
from array import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

m200 = []
stellarmass = []
rad3D = []
faceonRadM = []
faceonRadL = []

finalhalfL = []

gas = []
IDArray = ["0053","0094","0125","0162","0163","0175","0189","0190","0204","0209","0215","0220",
           "0224","0227","0259","0290","0300","0305","0329","0380","0408","0501","0549","0616",
           "0664","0721","0858","0908","0948"]
 
rootdir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'
for root,dirs,files in os.walk(rootdir):
    for IDs in IDArray:
        for each in dirs:
            #if the halos match our IDs (they all will, the reason we're doing this is so that
            #we stay in order. Otherwise if we rely on os.walk, it won't necessarily be in the
            #same order as our isophotelists files
            if each[1:] == IDs:
                #tempdir is the path of that halo directory
                tempdir = rootdir + each
                for one, two, three in os.walk(tempdir):
                    for each in three:
                        #get the info file we need for the given traits
                        if each == 'info_'+ z + '.txt':
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

smaArray = open('/home/sss274/Work/' + cosmodir + 'isophotelists/' + str(npix) + '/' + z[1:] + 'halflightSMA.txt')
counter = 0
finalhalfL = smaArray.read().splitlines()

smaArray.close()

final = np.dstack((IDArray,m200,stellarmass,gas,rad3D,faceonRadM,faceonRadL,finalhalfL))

#convert all the numbers to floats
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
tableName = 'haloTable' + z[1:] + '_' + str(npix)
np.save(tableName, final)

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

fig.savefig('/home/sss274/Work/' + cosmodir + str(npix) + '_halfLR_PDvsFSPSrads_info' + z + '.png')

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
fig.savefig('/home/sss274/Work/' + cosmodir + str(npix) + '_HalfLightFSPSvPDinfo' + z + '.png')

