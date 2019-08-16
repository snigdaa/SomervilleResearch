#halo = "m0094"
npix = 1026
setr = 50
z = '044'
cosmodir = 'cosmo_nodust_44/'
image_width = 40 #kpc default value, we'll check each halo's parameters master file to correct imagewidth

import os
haloarray = [name for name in os.listdir(".") if name[6:] == str(npix) + "px"]
#for the above loop to work this file must be in the same folder as the halo files
#otherwise change the listdir to the full path of where the halos are

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

for halo in haloarray:
    m = ModelOutput('/home/sss274/Work/' + cosmodir + halo[:5] + '_' + str(npix) + 'px/' + halo[:5] + '.' + z + 'v.rtout.image')

    halodir = "./" + halo + "/"
    for root,dirs,files in os.walk(halodir):
        for filename in files:
            if filename == "parameters_master.py":
                f = open(halodir + filename)
                for idx, value in enumerate(list(f)):
                    if value[:12] == "zoom_box_len":
                        image_width = value[15:17]
                        #get the specific image width for each halo
        

    filters = np.loadtxt('/home/sss274/Work/Vfiles/V_johnson.txt')
    thru = np.loadtxt('/home/sss274/Work/Vfiles/V_thruput.txt', dtype='double')
    redshift = 0.064

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
    center = npix/2
    loggedAr =  np.log10(totShowVal[center-setr:center+setr,center-setr:center+setr]*100000.0 + 0.01)

    img = plt.imshow(loggedAr, cmap='Spectral', interpolation='nearest')

    fig.savefig('/home/sss274/Work/' + cosmodir + 'ImagesPrefit/' + str(npix) + "/" + halo + '.png', bbox_inches='tight',dpi=300)

    
