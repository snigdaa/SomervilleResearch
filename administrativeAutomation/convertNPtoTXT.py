import numpy as np
import os

loaded = np.load('haloTable44.npy')

f = open('haloTable44.txt','a')
for idx, val in enumerate(loaded):
    f.write(str(val) + "\n")
    print str(val)+"\n"
