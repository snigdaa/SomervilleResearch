import os
from shutil import copyfile,move,copy
import numpy as np

halfLradii = np.loadtxt('/home/sss274/Work/isophotelists/44halflightRADIUS.txt')
doneFiles = ['02','09','10','11','12','13','14','15','16','18','19','20','21','22','23','24','25','26','27','28','29']

doneRight = ['02','09','10','11','16','18','19','20','21','23','24','25']

rootdir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'
haloDirectory = '/home/sss274/Work/cosmo35/'
haloList = os.listdir(haloDirectory)
m200 = []
stellarmass = []
faceonRadM = np.zeros(21,dtype=float)
faceonRadL = np.zeros(21,dtype=float)
unableorable = [0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1]
IDArray = []
roots = os.listdir(rootdir)
finalhalfL = np.zeros(21,dtype=float)
rad3D = np.zeros(21,dtype=float)

for idx, val in enumerate(haloList):
    for indexes, each in enumerate(doneFiles):
        if each == val[0:2]:
            haloID = val[5:10]
            IDArray.append(haloID)
            print haloID
            print IDArray
            for number, ID in enumerate(roots):
                if ID == val[5:10]:
                    hydrodir = rootdir+val[5:10]+'/'
                    info = os.listdir(hydrodir)
                    for num,files in enumerate(info):
                        if files == 'info_044.txt':
                            f = open(hydrodir+'/'+files, 'r')
                            for linenum, line in enumerate(list(f)):
                                if linenum==11:
                                    m200[indexes] = line[21:33]
                                if linenum==14:
                                    stellarmass[indexes] = line[21:33]
                                if linenum==24:
                                    rad3D[indexes]=line[21:33]
                                if linenum==25:
                                    faceonRadM[indexes]=line[21:33]
                                if linenum==26:
                                    faceonRadL[indexes]=line[21:33]

#halfLradii: array made from np.loadtxt of calculated L raadii
#finalhalfL: final array including negative spots for unfinished calcs
#temphalfL = np.empty(12,dtype=float)
#for num, each in enumerate(doneRight):
#    temphalfL[num]=halfLradii[num]

print haloList
print IDArray
#print finalhalfL
            
#for root, dirs, files in os.walk(haloDirectory):
#    for indexes, each in enumerate(doneFiles):
#        print each
#        if each == dirs[0:2]:
#            print each
#final = open('finalTable.txt', 'w')

