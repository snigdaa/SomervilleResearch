import numpy as np
import pygad as pg
import pygad.plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pygad.environment import module_dir
from pygad.snapshot import Snap
import os
import math

# Loading file keywords (you can loop these over in the future :)
model = 'MrAGN'
haloid = 'm0053'
snap_nums = '88'

# Define snapshot file and trace file (info*.txt)
snap_filename = '/Volumes/Happy/Choi16_Fiducial/Fiducial_'+model+'_hdf5/'+haloid+'/snap_'+haloid+'_sf_x_2x_0' + snap_nums+'.hdf5'
trace_filename = '/Volumes/Happy/Choi16_Fiducial/Fiducial_'+model+'_hdf5/'+haloid+'/info_0'+snap_nums+'.txt'

# Load snapshot file
s=pg.Snap(snap_filename, load_double_prec=True,physical=False)
print s
# Load info file
info = pygad.tools.read_info_file(trace_filename)
center = info['center'] # take the center coordinate

# Translate the snapshot to be centered at the trace file center
pygad.Translation(-center).apply(s)
s.to_physical_units()

# check the star particle quantities
s.stars

# Define empty dict to save 2d grid
maps = {}

# plot the image of stars, with given extent and number of pixels (Npx), with the quantity 'mass' (we need to take mass for the projected mass plot). The created 2d grid is saved in dictionary 'maps'.
fig,ax,im,cbar = pg.plotting.image(s.stars,extent='20 kpc',Npx=200,qty='mass',
                                   surface_dens=False,maps=maps,softening = pg.UnitArr([0,2,5,10,0.555,1],'kpc'));
#plt.savefig(haloid + '_starmap.png')
arr = maps['qty']
print 'original array center?'
print arr[95:105,95:105]
np.savetxt('./starmapFiles/numpyArraystxt/' + haloid + 'projarray.txt',arr)
    
center = 100
setr = 40

data = np.log10(arr[center-setr:center+setr,center-setr:center+setr]*100000.0+0.01)
data_nonlog = arr[center-setr:center+setr,center-setr:center+setr]/1e7
print 'data logged?'
print data
print 'data nonlogged?'
print data_nonlog

import photutils
from photutils.isophote import Ellipse
from photutils import data_properties, properties_table, EllipticalAperture, aperture_photometry

ellipse = Ellipse(data)

positions = (100,100)

isolist = ellipse.fit_image()
    
smas = isolist.sma
eps = isolist.eps
flux = isolist.tflux_e
pas = isolist.pa
xcent = isolist.x0
ycent = isolist.y0

x = flux[len(flux)-1]/2.0

fluxinterp = np.interp(x, flux, smas)

print 'interpolated sma pix val: ', fluxinterp

e = np.interp(x, flux, eps)
    
print 'interpolated ellipticity val: ', e

#ellipse gives it in degrees from +y, ellipticalaperture needs it in radians 
#from +x so we are converting here
#theta = (np.interp(x,flux,pas) + 90)*(math.pi/180)
theta = np.zeros_like(pas)
for idx,val in enumerate(pas):
    theta[idx] = (val+90)*(math.pi/180)
#print 'interpolated rot angle: ', theta

sna = fluxinterp*np.sqrt(1-(e**2))

y = np.zeros_like(smas)
for idx, val in enumerate(smas):
    y[idx] = x

rad = np.zeros_like(flux)
for idx, val in enumerate(flux):
    rad[idx] = fluxinterp

combined = np.zeros((len(xcent),2))
for idx, val in enumerate(xcent):
    combined[idx,0] = val
    combined[idx,1] = ycent[idx]
print(combined)

minor =np.zeros_like(smas)
for idx,val in enumerate(smas):
    minor[idx] = smas[idx]*np.sqrt(1-(eps[idx]**2))

apertures = EllipticalAperture(combined,smas,minor,theta)
phot_table = aperture_photometry(data,apertures)
phot_table['aperture_sum'].info.format = '%.8g'
print(phot_table.shape)
#fig,ax = plt.subplots()
#phot_table.plot(origin = (0,0),ax=ax)
#fig.savefig('THISISATEST.png')
 
