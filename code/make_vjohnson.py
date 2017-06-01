import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u


# ------------------------
# modifiable header
# ------------------------

filters = np.loadtxt('~/Work/Vfiles/V_johnson.txt')
thru = np.loadtxt('~/Work/Vfiles/V_thruput.txt', dtype='double')

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


#ax = fig.add_subplot(111)

#calculate image width in kpc
#w = image.x_max * u.cm
#w = w.to(u.kpc)

#finalArr = np.empty_like(image[:,:,0])
totShowVal = image.val[0, :, :, 0]
for idx, fil in enumerate(filters):
    wav = fil
    
    #find nearest wavelength
    iwav = np.argmin(np.abs(wav - image.wav))
    throughput = thru[idx]

    #add up all the image wavelength vals
    totShowVal += (image.val[0, :, :, iwav])*throughput
    
#plot the beast
#cax = ax.imshow(np.log(totShowVal), cmap = plt.cm.spectral, origin='lower', extent=[-w.value, w.value, -w.value, w.value])

loggedAr = np.log(totShowVal)
finalImg = plt.imshow(loggedAr)

fig.savefig('pd_image_vjNew.png')

#cax = ax.imshow(np.log(totShowVal), cmap = plt.cm.spectral)


#plt.xlim([-image_width,image_width])
#plt.ylim([-image_width,image_width])


# Finalize the plot
#ax.tick_params(axis='both', which='major', labelsize=10)
#ax.set_xlabel('x kpc')
#ax.set_ylabel('y kpc')

#plt.colorbar(cax,label='Flux (mJy)',format='%.0e')

#fig.savefig('pd_image_vjNew.png')
