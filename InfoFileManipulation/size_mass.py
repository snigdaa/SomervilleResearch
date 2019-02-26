import matplotlib
matplotlib.use('Agg')
import numpy as np
import scipy as sp
import matplotlib as mp
import os
#94 - z = 0.1
#44 z = 1.0
#27 z = 2.0 

#scan through Fiducial directory, through each halo directory for info files, then modify as necessary. 

rootdir = '/Volumes/Happy/Choi16_Fiducial/Fiducial_MrAGN/'
z_0array = np.zeros((1,8))
z_1array = np.zeros((1,8))
z_2array = np.zeros((1,8))
numArray = np.zeros((1,8))

#iterate through rootdir
#os.walk method: for root, dirs, files in os.walk(rootdir) give root, dirs, and files in '' strings. 
#for dirpath, dirs, files in os.walk(rootdir):
    #iterate through directories in rootdir
#    for each in dirs:
        #iterate through files in subdirectories of rootdir
#        for halodir, halodirs, txtfiles in os.walk(each):
            #look only for files containing info for z=0,1,2
#            if txtfiles == 'info_027.txt' or txtfiles == 'info_044.txt' or txtfiles == 'info_094.txt':
#                theFile = np.genfromtxt(txtfiles, skiprows = 1, delimiter = (21,13))
 
haloList = os.listdir(rootdir)
for halo in haloList:
    if os.path.isdir(rootdir+halo):
        files = os.listdir(rootdir+halo)
        for txtfiles in files:
            if txtfiles == 'info_027.txt' or txtfiles == 'info_044.txt' or txtfiles == 'info_094.txt':
                theFile = np.genfromtxt(rootdir+halo+'/'+txtfiles, delimiter = (21,13))
                r200=theFile[7,1]
                numArray[:,0]=r200
                m200=theFile[8,1]
                numArray[:,5]=m200
                r500=theFile[9,1]
                numArray[:,1]=r500
                m500=theFile[10,1]
                numArray[:,6]=m500
                mstars = theFile[11,1]
                numArray[:,7]=mstars
                reff = theFile[23,1]
                numArray[:,2]=reff
                rh3d = theFile[21,1]
                numArray[:,3]=rh3d
                rhface = theFile[22,1]
                numArray[:,4]=rhface

                #numArray = [r200, r500, reff, rh3d, rhface, m200, m500, mstars]

                if txtfiles == 'info_027.txt':
                    z_2array = np.append(z_2array, numArray, axis=0)
                elif txtfiles == 'info_044.txt':
                    z_1array = np.append(z_1array, numArray, axis=0)
                elif txtfiles == 'info_094.txt':
                    z_0array = np.append(z_0array, numArray, axis=0)
                
np.savetxt('infoparamz0.txt', z_0array)
np.savetxt('infoparamz1.txt', z_1array)
np.savetxt('infoparamz2.txt', z_2array)

#filenum = 11
#f=""

#/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/m0948
#/Volumes/Happy/Choi16_Fiducial/Fiducial_MrAGN

#finalArray=np.zeros((3,8))
#while filenum < 95:
#    if filenum >= 11 and filenum <95:
#        f = '/Volumes/Happy/Choi16_Fiducial/Fiducial_MrAGN/m0053/info_0'+str(filenum)+'.txt'
#    else:
#        f = '/Volumes/Happy/Choi16_Fiducial/Fiducial_MrAGN/m0053/info_'+str(filenum)+'.txt'

#    filenum+=1
    
#    if filenum == 94 or filenum == 44 or filenum == 27:

#        theFile = np.genfromtxt(f, skiprows=1, delimiter=(21, 13))

#        r200=theFile[8,1]
#        m200=theFile[9,1]
#        r500=theFile[10,1]
#        m500=theFile[11,1]
#        mstars = theFile[12,1]
#        reff = theFile[24,1]
#        rh3d = theFile[22,1]
#        rhface = theFile[23,1]

#        numArray = [r200, r500, reff, rh3d, rhface, m200, m500, mstars]
        
#        if filenum==27:
#            finalArray[0] = numArray
#        if filenum==44:
#            finalArray[1] = numArray
#        if filenum == 94:
#            finalArray[2] = numArray

#np.savetxt('infoparamm0053.txt', finalArray)
