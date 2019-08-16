import numpy as np
import os

loaded = np.load('haloTable44_512.npy')

f = open('haloTable44_512.txt','a')
for idx, val in enumerate(loaded):
    f.write(str(val) + "\n")
    print str(val)+"\n"
