halo = "m0948"
npix = 512
setr = 50
z = '044'
cosmodir = 'cosmo_nodust_44/'
image_width = 40 #kpc default value, we'll check each halo's parameters master file to correct imagewidth

import os
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
import pandas as pd

# ------------------------
# modifiable header
# ------------------------


m = ModelOutput('/home/sss274/Work/' + cosmodir + halo + '_' + str(npix) + 'px/' + halo + '.' + z + 'v.rtout.image')

halodir = "./" + halo + "_" + str(npix) + "px/"
for root,dirs,files in os.walk(halodir):
    for filename in files:
        if filename == "parameters_master.py":
            f = open(halodir + filename)
            for idx, value in enumerate(list(f)):
                if value[:12] == "zoom_box_len":
                    image_width = value[15:17]
                    #get the specific image width for each halo
                    floatImage = float(image_width)*2
                    convert = floatImage/npix
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
loggedData =  np.log10(totShowVal[center-setr:center+setr,center-setr:center+setr]*100000.0 + 0.01)
nonloggedData =  totShowVal[center-setr:center+setr,center-setr:center+setr]*(10**6)

img = plt.imshow(loggedData, cmap='Spectral', interpolation='nearest')

#I've commented this out because I've created all the images already and am only interested in getting
#the images after fitting right now
#fig.savefig('/home/sss274/Work/' + cosmodir + 'ImagesPrefit/' + str(npix) + "/" + halo + '.png', bbox_inches='tight',dpi=300)

from photutils.isophote import Ellipse
ellipse = Ellipse(loggedData)
ellipse_nonlog = Ellipse(nonloggedData)

isolist = ellipse.fit_image()
isolist_nonlog = ellipse_nonlog.fit_image()

fig, (ax1, ax2) = plt.subplots(figsize=(12, 5), nrows=1, ncols=2)
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.10, top=0.91)
ax1.imshow(loggedData, origin='lower')

smas = np.linspace(5, 40, 20)
for sma in smas:
    iso = isolist.get_closest(sma)
    x, y, = iso.sampled_coordinates()
    ax1.plot(x, y, color='white')

ax1.set_xlim([0,100])
ax1.set_ylim([0,100])

ax2.plot(isolist_nonlog.sma, isolist_nonlog.tflux_e, marker='o', markersize=4)
ax2.set_xlabel('Semimajor Axis Length $(pix)$')
ax2.set_ylabel('Flux $(kpc)$')

print 'sma:',isolist_nonlog.sma
print 'tflux:', isolist_nonlog.tflux_e

smas = isolist_nonlog.sma
eps = isolist_nonlog.eps
flux = isolist_nonlog.tflux_e

if len(flux) == 0:
    x = 0
else:
    x = flux[len(flux)-1]/2.0
print x

IsoTable = isolist_nonlog.to_table()
print 'table of isophote data:', IsoTable.pprint(max_lines=100)

if x == 0:
    fluxinterp = 0
    e = 0
else:
    fluxinterp = np.interp(x, flux, smas)
    e = np.interp(x, flux, eps)

print 'interpolated sma pix val: ', fluxinterp

print 'interpolated ellipticity val: ', e

#value of semiminor axis
sna = fluxinterp*np.sqrt(1-(e**2))

#value of equivalent radius
radius = np.sqrt(sna*fluxinterp)

#y = half-light value
y = np.zeros_like(smas)
for idx, val in enumerate(smas):
    y[idx] = x

#rad = sma pixel value
rad = np.zeros_like(flux)
for idx, val in enumerate(flux):
    rad[idx] = fluxinterp

#add to flux plot
ax2.plot(smas, y, label= "half-light flux")
ax2.plot(rad, flux, color = "red", label= "half-light radius")
ax2.legend(loc='lower right', bbox_to_anchor=(1,0))

#add to image plot
iso = isolist.get_closest(fluxinterp)
#^^get closest sma, since that's what isolist has already calculated
x, y = iso.sampled_coordinates()
ax1.plot(x,y, color = "black")
ax1.set_axis_off()

fig.savefig('/home/sss274/Work/' + cosmodir + 'ISOPHOTALFITIMAGES/' + str(npix) + "/" + halo + 'iso_' + str(npix) + '.png')

#calculate half-light radius in kpc values
smakpcval = fluxinterp*convert
radkpcval = radius*convert
snakpcval = sna*convert
print "sma kpc", smakpcval
print "rad kpc", radkpcval
print "semiminor kpc", snakpcval

rootname = '/home/sss274/Work/' + cosmodir + 'isophotelists/' +  str(npix) + "/" 

file_name = rootname + z[1:] + "halflightSMA.txt"
file = open(file_name, 'a')
file.write(str(smakpcval) + "\n")

file_name = rootname + z[1:] + "isophoteELLIPTICITY.txt"
file = open(file_name, 'a')
file.write(str(e) + "\n")

file_name = rootname + z[1:] + "halflightSemiMinor.txt"
file = open(file_name, 'a')
file.write(str(snakpcval) + "\n")

file_name = rootname + z[1:] + "halflightRADIUS.txt"
file = open(file_name, 'a')
file.write(str(radkpcval) + "\n")

eps = isolist_nonlog.eps
eps_err = isolist_nonlog.ellip_err
grad = isolist_nonlog.grad
grad_err = isolist_nonlog.grad_error
intensity = isolist_nonlog.intens
int_err = isolist_nonlog.int_err
ndata = isolist_nonlog.ndata
npix_c = isolist_nonlog.npix_c
npix_e = isolist_nonlog.npix_e
pa = isolist_nonlog.pa
pa_err = isolist_nonlog.pa_err
rms = isolist_nonlog.rms
sma = isolist_nonlog.sma
tflux_c = isolist_nonlog.tflux_c
tflux_e = isolist_nonlog.tflux_e

indiv_table = np.column_stack((eps,eps_err,grad,grad_err,intensity,int_err,ndata,npix_c,npix_e,pa,pa_err,rms,sma,tflux_c,tflux_e))
finaltable = pd.DataFrame(indiv_table,columns=['ellipticity', 'ellipticity error', 'radial intensity grad', 'gradient error',
                                               'intensity', 'intensity error', 'ndata', 'npix_c', 'npix_e', 'position angle (rad)',
                                               'pa error (rad)', 'rms of intensity values', 'sma (px)', 'tflux_c', 'tflux_e'])

print finaltable

dstring = finaltable.to_string()
fname = rootname + "isoSummaries/" + halo + ".txt"

f = open(fname, 'w')
f.write(dstring)
f.close()

