import os.path
from shutil import copy
import numpy as np
import os

base = '/home/sss274/Work/cosmo/'
hydrodir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'

newbase = '/home/sss274/Work/cosmo50/'

#make folders for all halos at 35 kpc
for root, dirs, files in os.walk(base):
    for name in dirs:
        if name[3:5]=='44':
            os.mkdir(os.path.join(newbase,name+'_50kpc'))
