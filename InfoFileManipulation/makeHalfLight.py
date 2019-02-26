import numpy as np
import scipy as sp
import os
from shutil import copyfile, move, copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#unsortedL = np.loadtxt('halflight.txt')
unsortedR = np.loadtxt('halflightRADIUS.txt')
numArray = [28,29,30,31,33,34,35,37,39,40,41,42,43,44,45] #halo run numbers, 50 kpc

rootdir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'
halodir = '/home/ec675/Work/pd/'
#halodest = '/home/sss274/Work/haloparam'
haloList = os.listdir(halodir)

#declare the unsorted array that will hold all info at the end
finalUnsorted = np.empty([15,6])

#declare sorted array as well for sorted with 3d mass, faceon mass, and light radii
finalSorted3d = np.empty([15,6])
finalSortedface = np.empty([15,6])
finalSortedlight = np.empty([15,6])

rad3d = np.empty([15,1])
radfaceon = np.empty([15,1])

haloArray = []
haloNum = 0

for idx, val in enumerate(haloList):
#look through powderday runs
    for indexes, each in enumerate(numArray):
#if we're looking at one of the 50 kpc runs:
        if str(each) == val[:2]:
            for root, dirs, files in os.walk(halodir + val):
#looking for the parameters_model file to get location of info files
                for eachfile in files:
                    if eachfile == 'parameters_model.py':
#copy parameter file into own directory to parse through file and get the same line from all parameter folders
#                        newName = os.path.join(halodest+'/'+str(each)+ '_' + eachfile)
#                        copy(halodir+val+'/'+eachfile, newName)
                        f = open(halodir+val+'/'+eachfile, 'r')
#go through parameter file and get location of info files
                        for idx, val in enumerate(list(f)):
                            if idx == 11:
                                haloName = val[-8:-2]
                                hydrodir = rootdir+haloName
                                info = os.listdir(hydrodir)
                                haloNum = haloName[-4:-1]
#get info from info files and put into array
                                for idx, val in enumerate(info):
                                    if val == 'info_088.txt':
#go to list idx 24 for R_half_M (3D)
#go to list idx 25 for R_half_M (faceon)
                                        f = open(hydrodir+val, 'r')
                                        for idx,line in enumerate(list(f)):
                                            if idx==24:
                                                rad3d[indexes] = line[21:33]
                                            if idx==25:
                                                radfaceon[indexes] = line[21:33]
                                        finalUnsorted[indexes]=[indexes, each, haloNum, unsortedL[indexes], rad3d[indexes], radfaceon[indexes]]
#^^organize all important values as follows:
#index (0,1,2...), halo# (28,29,30...), halo name (948,858,721...), 
#halflight R [kpc] (7.59, 7.75, 1.18...), halfM 3d (5.9, 5.2, 5.5...), 
#halfM faceon (4.36, 3.83, 4.37...)

#sort the array by increasing half-mass 3D
orderfinalSorted = finalUnsorted[:,4].argsort() 
#returns array of indices from finalUnsorted in the order that would be sorted
for idx, val in enumerate(orderfinalSorted):
    finalSorted3d[idx] = finalUnsorted[val]

#sort the array by increasing half-mass faceon
orderfinalSorted = finalUnsorted[:,5].argsort()
for idx,val in enumerate(orderfinalSorted):
    finalSortedface[idx] = finalUnsorted[val]

#PLOT HALF-MASSES VS HALF-LIGHT

fig, (ax1,ax2,ax3) = plt.subplots(figsize = (18,6), nrows=1, ncols=3)
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.9)
ax1.scatter(finalSorted3d[:,4],finalSorted3d[:,3], color='g',marker='s')
ax2.scatter(finalSortedface[:,5],finalSortedface[:,3], color='g', marker='o')
ax3.scatter(finalSorted3d[:,4],finalSorted3d[:,3], color='r',marker='s', label='3D model')
ax3.scatter(finalSortedface[:,5],finalSorted3d[:,3], color='b',marker='o', label='Face-on projection')
ax1.set_xlabel(r'Half-mass R from 3D model ($ckpc/h_{0}$)', fontsize = 18)
ax2.set_xlabel('Half-mass R from face-on projection ($ckpc/h_{0}$)', fontsize = 18)
ax3.set_xlabel('Half-mass R ($ckpc/h_{0}$)', fontsize = 18)
ax1.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax2.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax3.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
fig.suptitle('Half-Mass R vs. Half-Light R', fontsize=20)

ax1.set_xlim(0,14)
ax2.set_xlim(0,14)
ax3.set_xlim(0,14)
ax3.set_ylim(0,2.5)
ax2.set_ylim(0,2.5)
ax1.set_ylim(0,2.5)

ax3.plot(np.linspace(0,14),np.linspace(0,14),color='g',linestyle='dashed',linewidth=2,label='ideal relation')
ax3.legend(loc='lower right',bbox_to_anchor=(1,0))

fig.savefig('halflightplotINCREASINGM.png')

#sort the array by increasing half-light
orderfinalSorted = finalUnsorted[:,3].argsort()
for idx,val in enumerate(orderfinalSorted):
    finalSortedlight[idx] = finalUnsorted[val]

fig2, (ax4,ax5,ax6) = plt.subplots(figsize = (18,6), nrows=1, ncols=3)
fig2.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.9)
ax4.scatter(finalSortedlight[:,4],finalSortedlight[:,3], color='g',marker='s')
ax5.scatter(finalSortedlight[:,5],finalSortedlight[:,3], color='g', marker='o')
ax6.scatter(finalSortedlight[:,4],finalSortedlight[:,3], color='r', label = '3D model',marker='s')
ax6.scatter(finalSortedlight[:,5],finalSortedlight[:,3], color='b',label='Face-on projection',marker='o')

ax4.set_xlabel('Half-mass R from 3D model ($ckpc/h_{0}$)' , fontsize = 18)
ax5.set_xlabel('Half-mass R from face-on projection ($ckpc/h_{0}$)', fontsize = 18)
ax6.set_xlabel('Half-mass R ($ckpc/h_{0}$)', fontsize = 18)
ax4.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax5.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax6.set_ylabel('Half-light R $(kpc)$', fontsize = 18)

ax4.set_xlim(0,14)
ax5.set_xlim(0,14)
ax6.set_xlim(0,14)
ax6.set_ylim(0,2.5)
ax5.set_ylim(0,2.5)
ax4.set_ylim(0,2.5)

ax6.plot(np.linspace(0,13),np.linspace(0,13),color='g',label='ideal relation',linestyle='dashed',linewidth=2)
fig2.suptitle('Half-Mass R vs. Half-Light R', fontsize=20)
ax6.legend(loc='lower right',bbox_to_anchor=(1,0))

fig2.savefig('halflightplotINCREASINGL.png')

#np.savetxt('/home/sss274/Work/code/halflightarrays/unsorted.txt',finalUnsorted)
#np.savetxt('/home/sss274/Work/code/halflightarrays/3dmasssorted.txt',finalSorted3d)
#np.savetxt('/home/sss274/Work/code/halflightarrays/facemassunsorted.txt',finalSortedface)
#np.savetxt('/home/sss274/Work/code/halflightarrays/lightsorted.txt',finalSortedlight)

#Plotting for thesis figures

fig, ax = plt.subplots(figsize = (6,6), nrows=1, ncols=1)
fig.subplots_adjust(left=0.12, right=0.98, bottom=0.13, top=0.9)
ax.scatter(finalSortedface[:,5],finalSortedface[:,3], color='b',label='Half-mass R vs. Half-light R',marker='o')
ax.set_xlabel('Half-mass R ($ckpc/h_{0}$)', fontsize = 18)
ax.set_ylabel('Half-light R $(kpc)$', fontsize = 18)
ax.set_xlim(0,13)
ax.set_ylim(0,2.5)
#plot with correction factor, ~0.15 based on galaxy set
y = np.linspace(0,13)
correction = np.zeros_like(y)
for idx, val in enumerate(y):
    correction[idx]=val*0.15+0.15

ax.plot(np.linspace(0,13),np.linspace(0,13),color='g', linestyle='dashed', linewidth=2,label=r'ideal relation $(f(x) = x)$')
ax.plot(np.linspace(0,13),correction,color='r', linestyle='dashed', linewidth=2,label=r'correction factor$(f(x) = 0.15x)$')
ax.legend(loc='lower right',bbox_to_anchor=(1,0))

fig.suptitle('Half-Mass R vs. Half-Light R', fontsize=20)
fig.savefig('/home/sss274/Work/code/thesis/TEST.png')
