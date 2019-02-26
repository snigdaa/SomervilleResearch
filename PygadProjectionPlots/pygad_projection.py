import numpy as np
import pygad as pg
import pygad.plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pygad.environment import module_dir
from pygad.snapshot import Snap
import os

# Loading file keywords (you can loop these over in the future :)
model = 'MrAGN'
#haloid = 'm0948'

dirpath = '/Volumes/Happy/Choi16_Fiducial/Fiducial_'+model+'_hdf5/'
#array of all the halo ids that you can loop over
#haloarray = [name for name in os.listdir(dirpath) if name[0]=='m']
haloarray = ['m0053','m0094','m0125','m0162','m0175','m0190','m0204','m0209','m0215','m0227','m0259','m0290','m0305','m0380','m0408','m0549','m0616','m0664','m0721','m0858','m0908','m0948']

snap_nums = '88'

for haloid in haloarray:
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
    fig,ax,im,cbar = pg.plotting.image(s.stars,extent='30 kpc',Npx=200,qty='mass',
                                       surface_dens=False,maps=maps,softening = pg.UnitArr([0,2,5,10,0.555,1],'kpc'));
    #plt.savefig('./starmapFiles/' + haloid + '_starmap.png')
    #print maps['qty']
    arr = maps['qty']
    print(arr.dtype)
    print arr[245:255,245:255]
    #np.savetxt('./starmapFiles/numpyArraystxt/' + haloid + 'projarray.txt',arr)

    center = 100
    setr = 40

    data = np.log10(arr[center-setr:center+setr,center-setr:center+setr]*100000.0+0.01)
    data_nonlog = arr[center-setr:center+setr,center-setr:center+setr]/1e7
    print 'data logged?'
    print data
    #print 'data nonlogged?'
    #print data_nonlog

    import photutils
    from photutils.isophote import Ellipse

    ellipse = Ellipse(data)
    ellipse_nonlog = Ellipse(data_nonlog)

    isolist = ellipse.fit_image()
    isolist_nonlog = ellipse_nonlog.fit_image()

    fig, (ax1, ax2) = plt.subplots(figsize=(12, 5), nrows=1, ncols=2)
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.10, top=0.91)
    ax1.imshow(data, origin='lower')
    
    smas = np.linspace(5, 40, 20)
    for sma in smas:
        iso = isolist_nonlog.get_closest(sma)
        x, y, = iso.sampled_coordinates()
        ax1.plot(x, y, color='white')
    #ax1.set_xlim([0,100])
    #ax1.set_ylim([0,100])

    ax2.plot(isolist_nonlog.sma, isolist_nonlog.tflux_e,
             marker='o', markersize=4)
    ax2.set_xlabel('Semimajor Axis Length $(pix)$')
    ax2.set_ylabel('Flux $(kpc)$')

    smas = isolist_nonlog.sma
    eps = isolist_nonlog.eps
    flux = isolist_nonlog.tflux_e
    x = flux[len(flux)-1]/2.0
    
    fluxinterp = np.interp(x, flux, smas)

    print 'interpolated sma pix val: ', fluxinterp

    e = np.interp(x, flux, eps)

    print 'interpolated ellipticity val: ', e

    sna = fluxinterp*np.sqrt(1-(e**2))

    radius = np.sqrt(sna*fluxinterp)

    y = np.zeros_like(smas)
    for idx, val in enumerate(smas):
        y[idx] = x

    rad = np.zeros_like(flux)
    for idx, val in enumerate(flux):
        rad[idx] = fluxinterp

    #add to flux plot
    ax2.plot(smas, y, label= "half-light flux")
    ax2.plot(rad, flux, color = "red", label= "half-light radius")
    ax2.legend(loc='lower right', bbox_to_anchor=(1,0))

    iso = isolist.get_closest(fluxinterp)

    x, y = iso.sampled_coordinates()
    ax1.plot(x,y, color = "black")
    ax1.set_axis_off()

    fig.savefig('./ProjPlot_IsophotalFits/' + haloid + 'isowithhalf88.png')

