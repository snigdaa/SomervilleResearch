halo = 'm0948'
import yt
import numpy as np
import yt.units as units
import pylab


fname = '/Users/snigdaa/Work/amarelFiles/snapFiles/snap_' + halo + '_sf_x_2x_088.hdf5'
#fname = 'snap_m0300_sf_x_2x_044.hdf5'

unit_base = {'UnitLength_in_cm' : 3.08568e+21,
             'UnitMass_in_g' : 1.989e+43,
             'UnitVelocity_in_cm_per_s' : 100000}

bbox_lim = 1e5 #kpc

bbox = [[-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim]]

ds = yt.load(fname,unit_base=unit_base, bounding_box=bbox)
ds.index
ad = ds.all_data()
density = ad[("PartType0","density")]
wdens = np.where(density == np.max(density))
coordinates = ad[("PartType0", "Coordinates")]
center = coordinates[wdens][0]
print ('center = ',center)

new_box_size = ds.quan(250, 'code_length')

left_edge = center - new_box_size/2
right_edge = center + new_box_size/2

box_size = new_box_size.in_units('Mpc')
left = left_edge.in_units('Mpc')
right = right_edge.in_units('Mpc')

ad2 = ds.region(center=center, left_edge=left_edge, right_edge=right_edge)

px = yt.ProjectionPlot(ds, 'x', ('gas', 'density'), center=center, width=new_box_size)
#px.show()
px.set_axes_unit('Mpc')
px.annotate_scale()
px.annotate_timestamp(redshift=True)
px.annotate_text([0.01,0.12], 'Plot width: ' + str(box_size), coord_system='axis')

px.save(halo + 'ProjectionPlot')
