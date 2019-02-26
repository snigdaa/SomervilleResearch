import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u
from photutils import centroid_com, centroid_1dg, centroid_2dg

# ------------------------
# modifiable header
# ------------------------

filters = np.loadtxt('V_johnson.txt')
thru = np.loadtxt('V_thruput.txt', dtype='double')

m = ModelOutput('/home/sss274/Work/Outputs/diskMerger/85/merger.085v.rtout.image')
redshift=2
image_width = 200 #kpc

# ------------------------


distance = Planck13.luminosity_distance(redshift).cgs.value


# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(distance=distance, units='mJy')

# Open figure and create axes
fig = plt.figure()


ax = fig.add_subplot(111)

#calculate image width in kpc
w = image.x_max * u.cm
w = w.to(u.kpc)

totShowVal = image.val[0, :, :, 0]
one = [0.0, 0.0]
two = [0.0, 0.0]
#tri = [0.0, 0.0]

for idx, fil in enumerate(filters):
    wav = fil 
    iwav = np.argmin(np.abs(wav - image.wav))
    throughput = thru[idx]
    l1,k1=centroid_com(image.val[0,:,:,iwav]*throughput)
    l2,k2=centroid_1dg(image.val[0,:,:,iwav]*throughput)
    #l3,k3=centroid_2dg(image.val[0,:,:,iwav]*throughput)
    if idx < filters.size-1:
        one[0] += l1
        one[1] += k1
        print one
        two[0] += l2
        two[1] += k2
        print two
        #tri[0] = l3
        #tri[1] = k3
print one, two
totX = ((one[0]/(filters.size-2))+(two[0]/(filters.size-2)))/2
totY = ((one[1]/(filters.size-2))+(two[1]/(filters.size-2)))/2

print totX, totY
