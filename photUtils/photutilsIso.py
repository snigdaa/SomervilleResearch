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
#21 is 10 kpc
#22 is 20 kpc
#m = ModelOutput('/home/ec675/Work/pd/21_cosmo_m0948_88_center/m0948.088.rtout.image')
#m = ModelOutput('/home/ec675/Work/pd/19_cosmo_m0948_88_Vband/m0948.088.rtout.image')4
halo = '11_'
m = ModelOutput('/home/sss274/Work/cosmo/' + halo + '44m0215/m0215.044v.rtout.image')
print halo

image_width = 100 #kpc
# 1 pixel represents 100/512 kpc
convert = image_width/512.0

# ------------------------
redshift = 0.06383
#all the SAME REDSHIFT, info_088
distance = Planck13.luminosity_distance(redshift).cgs.value

# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(distance=distance, units='mJy')
#print 'image value:'
# Open figure and create axes
fig = plt.figure()

totShowVal = image.val[0, :, :, 0]
#print totShowVal
#for each filter value in filter file
for idx, fil in enumerate(filters):
    #wavelength is equal to value at that line
    wav = fil
        
    #find nearest wavelength in image
    iwav = np.argmin(np.abs(wav - image.wav))
    throughput = thru[idx]

    #add up all the image wavelength vals
    totShowVal += (image.val[0, :, :, iwav])*throughput
    #print fil, iwav, throughput, (image.val[0, 256, 256, iwav])*throughput, image.val[0, 0, 0, iwav]

print totShowVal
#print totShowVal.shape
#plot the beast
#print totShowVal[256,256]
#print totShowVal
#loggedAr = np.log(totShowVal+1e-8)

#save np arrays to files for future use
#np.save(loggedAr, loggedAr)
#np.save(totAr, totShowVal)
center = 256
setr = 50

data = np.log10(totShowVal[center-setr:center+setr,center-setr:center+setr]*100000.0 + 0.01)#loggedAr
data_nonlog = totShowVal[center-setr:center+setr,center-setr:center+setr]*100000.0
print data
print data_nonlog
#print data_nonlog[50,50]

#from photutils.isophote import EllipseGeometry
#geometry = EllipseGeometry(x0=setr, y0=setr, sma=2., eps=0.5, pa=20.*np.pi/180)

#aper = EllipticalAperture((geometry.x0, geometry.y0), geometry.sma, geometry.sma*(1-geometry.eps), geometry.pa)
#defining your parameters, just initial fit^
from photutils.isophote import Ellipse
#print 'how far?'
ellipse = Ellipse(data)
#putting data and geometry together in one ellipse image
ellipse_nonlog = Ellipse(data_nonlog)

isolist = ellipse.fit_image()
#print isolist
#print(isolist.pa)

isolist_nonlog = ellipse_nonlog.fit_image()
#print isolist_nonlog


fig, (ax1, ax2) = plt.subplots(figsize=(12, 5), nrows=1, ncols=2)
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.10, top=0.91)
ax1.imshow(data, origin='lower')
#aper.plot(color='black') # this is for the initial "estimated" ellipse

smas = np.linspace(5, 40, 20)
for sma in smas:
    iso = isolist.get_closest(sma)
    x, y, = iso.sampled_coordinates()
    ax1.plot(x, y, color='white')
ax1.set_xlim([0,100])
ax1.set_ylim([0,100])

ax2.plot(isolist_nonlog.sma, isolist_nonlog.tflux_e,
             marker='o', markersize=4)
ax2.set_xlabel('Semimajor Axis Length $(pix)$')
ax2.set_ylabel('Flux $(kpc)$')

#print 'sma:',isolist_nonlog.sma
#print 'tflux:', isolist_nonlog.tflux_e

smas = isolist_nonlog.sma
eps = isolist_nonlog.eps
flux = isolist_nonlog.tflux_e
x = flux[len(flux)-1]/2.0
#value of maxluminosity

fluxinterp = np.interp(x, flux, smas)

print 'interpolated sma pix val: ', fluxinterp

e = np.interp(x, flux, eps)

print 'interpolated ellipticity val: ', e

sna = fluxinterp*np.sqrt(1-(e**2))

radius = np.sqrt(sna*fluxinterp)

#y = half-light value
y = np.zeros_like(smas)
for idx, val in enumerate(smas):
    y[idx] = x
#x = sma value
rad = np.zeros_like(flux)
for idx, val in enumerate(flux):
    rad[idx] = radius

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

fig.savefig('/home/sss274/Work/code/thesis/' + halo + 'isowithhalf.png')

#calculate half-light radius in kpc values
#smakpcval = fluxinterp*convert
#radkpcval = radius*convert
#snakpcval = sna*convert

#file_name = "halflightSMA.txt"
#file = open(file_name, 'a')
#file.write(str(smakpcval) + "\n")

#file_name = "isophoteELLIPTICITY.txt"
#file = open(file_name, 'a')
#file.write(str(e) + "\n")

#file_name = "isophoteSemiMinor.txt"
#file = open(file_name, 'a')
#file.write(str(snakpcval) + "\n")

#file_name = "halflightRADIUS.txt"
#file = open(file_name, 'a')
#file.write(str(radkpcval) + "\n")
