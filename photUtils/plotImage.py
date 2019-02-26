import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u
import photutils
from photutils import data_properties, properties_table, EllipticalAperture
from astropy.io import fits


# ------------------------
# modifiable header
# ------------------------

filters = np.loadtxt('/home/sss274/Work/Vfiles/V_johnson.txt')
thru = np.loadtxt('/home/sss274/Work/Vfiles/V_thruput.txt', dtype='double')
halo = '03_44m0125'
#m = ModelOutput('/home/ec675/Work/pd/' + halo + '_50kpc/' + halo[3:] + '.088v.rtout.image')
m = ModelOutput('/home/sss274/Work/cosmo40/03_44m0125_40kpc/m0125.044v.rtout.image')
#m = ModelOutput('/home/ec675/Work/pd/'+halo+'_z1_re/'+halo[3:]+'.044v.rtout.image')
redshift = 1
image_width = 40 #kpc

# ------------------------
distance = Planck13.luminosity_distance(redshift).cgs.value

# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(distance=distance, units='mJy')

# Open figure and create axes
fig = plt.figure()

totShowVal = image.val[0, :, :, 0]
#for each filter value in filter file
for idx, fil in enumerate(filters):
    #wavelength is equal to value at that line
    wav = fil
    
    #find nearest wavelength in image
    iwav = np.argmin(np.abs(wav - image.wav))
    throughput = thru[idx]

    #add up all the image wavelength vals
    totShowVal += (image.val[0, :, :, iwav])*throughput
    
#plot the beast
center = 256
setr = 100
loggedAr =  np.log10(totShowVal[center-setr:center+setr,center-setr:center+setr]*100000.0 + 0.01)

#save np arrays to files for future use
#np.save(loggedAr, loggedAr)
#np.save(totAr, totShowVal)


#props = data_properties(totShowVal)
#columns = ['id', 'xcentroid', 'ycentroid', 'semimajor_axis_sigma', 'semiminor_axis_sigma', 'orientation']
#position = (props.xcentroid.value, props.ycentroid.value)

#r = 2
#a = props.semimajor_axis_sigma.value * r
#b = props.semiminor_axis_sigma.value * r
#theta = props.orientation.value

#apertures = EllipticalAperture(position, a, b, theta=theta)
img = plt.imshow(loggedAr, cmap='Spectral', interpolation='nearest')

fig.savefig('/home/sss274/Work/images/galImages/44/' + halo + '_npimage.png', bbox_inches='tight',dpi=300)
