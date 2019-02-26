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

filters = np.loadtxt('~/Work/Vfiles/V_johnson.txt')
thru = np.loadtxt('~/Work/Vfiles/V_thruput.txt', dtype='double')

m = ModelOutput('/home/sss274/Work/Outputs/cosmological/88/m0948.088v.rtout.image')
redshift=0.1
image_width = 200 #kpc

# ------------------------
distance = Planck13.luminosity_distance(redshift).cgs.value

# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(distance=distance, units='mJy')

# Open figure and create axes
fig = plt.figure()

totShowVal = image.val[0, :, :, 0]
for idx, fil in enumerate(filters):
    wav = fil
    
    #find nearest wavelength
    iwav = np.argmin(np.abs(wav - image.wav))
    throughput = thru[idx]

    #add up all the image wavelength vals
    totShowVal += (image.val[0, :, :, iwav])*throughput
    
#plot the beast
loggedAr = np.log(totShowVal)

props = data_properties(totShowVal)
columns = ['id', 'xcentroid', 'ycentroid', 'semimajor_axis_sigma', 'semiminor_axis_sigma', 'orientation']
position = (props.xcentroid.value, props.ycentroid.value)

r = 2
a = props.semimajor_axis_sigma.value * r
b = props.semiminor_axis_sigma.value * r
theta = props.orientation.value

apertures = EllipticalAperture(position, a, b, theta=theta)
img = plt.imshow(totShowVal, cmap='Spectral', interpolation='nearest')
finalImg = apertures.plot(color='#898989')

fig.savefig('isophot_v88.png', bbox_inches='tight',dpi=300)
