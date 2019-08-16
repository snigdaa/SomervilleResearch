import os.path
from shutil import copy
import numpy as np
import os
import shutil

base = '/home/sss274/Work/cosmo/'
#hydrodir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'

newbase = '/home/sss274/Work/cosmo_nodust_44/'
npix = 256

#make folders for all halos
for root, dirs, files in os.walk(base):
    for name in dirs:
        if name[3:5]=='44':
            srcDir = os.path.join(base,name) + '/'
            halodir = os.path.join(newbase,name[5:]+'_' + str(npix) + 'px')
            os.mkdir(halodir)
            shutil.copy(srcDir + 'parameters_master.py', halodir + '/.')
            os.rename(halodir+'/parameters_master.py', halodir+'/parameters_mastertest.py')

            shutil.copy(srcDir + 'parameters_model.py', halodir + '/.')
            os.rename(halodir+'/parameters_model.py', halodir+'/parameters_modeltest.py')

            shutil.copy(srcDir + 'pd.cmd', halodir + '/.')
            os.rename(halodir+'/pd.cmd', halodir+'/pdR.cmd')
            
