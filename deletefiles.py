import os.path
from shutil import copy
import numpy as np
import os
import shutil

base = '/home/sss274/Work/cosmo_nodust_44/'

for root,dirs,files in os.walk(base):
    for name in dirs:
        #newbase = os.path.join(base,name)
        #for halo,dirs,files in os.walk(newbase):
        #    for param in files:
        #        if param == 'parameters_master.py' or param == 'parameters_model.py' or param == 'pd.cmd':
        #            print(os.path.join(newbase,param))
        #            os.remove(os.path.join(newbase,param))
        shutil.rmtree(os.path.join(base,name))
