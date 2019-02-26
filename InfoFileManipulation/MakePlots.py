import numpy as np
import scipy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

theFile = np.loadtxt('infoparamz2.txt',skiprows=1)

#plot all M vs R_eff

x1 = theFile[:,7]
x2 = theFile[:,6]
x3 = theFile[:,5]
y = theFile[:,2]

plt.figure()
plt.subplot(111)
plt.xlabel('Mass')
plt.ylabel('R_eff')

plt.plot(x1, y, 'go', label="M_stars vs. Effective Radius")
plt.plot(x2, y, 'bo', label="M500 vs. Effective Radius")
plt.plot(x3, y, 'ro', label="M200 vs. Effective Radius")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('Mass_Reff.png', loc = '5', bbox_inches="tight", additional_artists=art, format='png')

#plot M_stars vs all R
y1 = theFile[:,0]
y2 = theFile[:,1]
y3 = theFile[:,2]
y4 = theFile[:,3]
y5 = theFile[:,4]
x = theFile[:,7]

plt.figure()
plt.subplot(111)
plt.xlabel('M_stars')
plt.ylabel('R')

plt.plot(x, y1, 'go', label="M_stars vs. R200")
plt.plot(x, y2, 'bo', label="M_stars vs. R500")
plt.plot(x, y3, 'ro', label="M_stars vs. R_eff")
plt.plot(x, y4, 'co', label="M_stars vs. R_half (3D)")
plt.plot(x, y5, 'ko', label="M_stars vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('Mstars_allR.png', format='png')

#plot M200 vs all R
y1 = theFile[:,0]
y2 = theFile[:,1]
y3 = theFile[:,2]
y4 = theFile[:,3]
y5 = theFile[:,4]
x = theFile[:,5]

plt.figure()
plt.subplot(111)
plt.xlabel('M200')
plt.ylabel('R')

plt.plot(x, y1, 'go', label="M200 vs. R200")
plt.plot(x, y2, 'ro', label="M200 vs. R500")
plt.plot(x, y3, 'bo', label="M200 vs. R_eff")
plt.plot(x, y4, 'co', label="M200 vs. R_half (3D)")
plt.plot(x, y5, 'ko', label="M200 vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('M200_allR.png', format='png')


#plot M500 vs all R
y1 = theFile[:,0]
y2 = theFile[:,1]
y3 = theFile[:,2]
y4 = theFile[:,3]
y5 = theFile[:,4]
x = theFile[:,6]

plt.figure()
plt.subplot(111)
plt.xlabel('M500')
plt.ylabel('R')

plt.plot(x, y1, 'go', label="M500 vs. R200")
plt.plot(x, y2, 'ro', label="M500 vs. R500")
plt.plot(x, y3, 'bo', label="M500 vs. R_eff")
plt.plot(x, y4, 'co', label="M500 vs. R_half (3D)")
plt.plot(x, y5, 'ko', label="M500 vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('M500_allR.png', format='png')

#plot R200 vs all Mass

x = theFile[:,0]
y1 = theFile[:,7]
y2 = theFile[:,6]
y3 = theFile[:,5]

plt.figure()
plt.subplot(111)
plt.xlabel('R200')
plt.ylabel('Mass')

plt.plot(x, y1, 'go', label="R200 vs. M_stars")
plt.plot(x, y2, 'bo', label="R200 vs. M500")
plt.plot(x, y3, 'ro', label="R200 vs. M200")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('R200_allMass.png', format='png')

#plot R500 vs all Mass

x = theFile[:,1]
y1 = theFile[:,7]
y2 = theFile[:,6]
y3 = theFile[:,5]

plt.figure()
plt.subplot(111)
plt.xlabel('R500')
plt.ylabel('Mass')

plt.plot(x, y1, 'go', label="R500 vs. M_stars")
plt.plot(x, y2, 'bo', label="R500 vs. M500")
plt.plot(x, y3, 'ro', label="R500 vs. M200")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('R500_allMass.png', format='png')

#plot rh3d vs all Mass

x = theFile[:,3]
y1 = theFile[:,7]
y2 = theFile[:,6]
y3 = theFile[:,5]

plt.figure()
plt.subplot(111)
plt.xlabel('R_half (3D)')
plt.ylabel('Mass')

plt.plot(x, y1, 'go', label="R_half (3D) vs. M_stars")
plt.plot(x, y2, 'bo', label="R_half (3D) vs. M500")
plt.plot(x, y3, 'ro', label="R_half (3D) vs. M200")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('RH3D_allMass.png', format='png')

#plot rhfaceon vs all Mass

x = theFile[:,4]
y1 = theFile[:,7]
y2 = theFile[:,6]
y3 = theFile[:,5]

plt.figure()
plt.subplot(111)
plt.xlabel('R_half (faceon)')
plt.ylabel('Mass')

plt.plot(x, y1, 'go', label="R_half (faceon) vs. M_stars")
plt.plot(x, y2, 'bo', label="R_half (faceon) vs. M500")
plt.plot(x, y3, 'ro', label="R_half (faceon) vs. M200")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('RHface_allMass.png', format='png')

#plot R200 vs all other R

x = theFile[:,0]
y1 = theFile[:,1]
y2 = theFile[:,2]
y3 = theFile[:,3]
y4 = theFile[:,4]

plt.figure()
plt.subplot(111)
plt.xlabel('R200')
plt.ylabel('All other R')

plt.plot(x, y1, 'go', label="R200 vs. R500")
plt.plot(x, y2, 'bo', label="R200 vs. R_eff")
plt.plot(x, y3, 'ro', label="R200 vs. R_half (3D)")
plt.plot(x, y4, 'co', label="R200 vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('R200_allR.png', format='png')

#plot R500 vs all other R

x = theFile[:,1]
y1 = theFile[:,0]
y2 = theFile[:,2]
y3 = theFile[:,3]
y4 = theFile[:,4]

plt.figure()
plt.subplot(111)
plt.xlabel('R500')
plt.ylabel('All other R')

plt.plot(x, y1, 'go', label="R500 vs. R200")
plt.plot(x, y2, 'bo', label="R500 vs. R_eff")
plt.plot(x, y3, 'ro', label="R500 vs. R_half (3D)")
plt.plot(x, y4, 'co', label="R500 vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('R500_allR.png', format='png')

#plot R_eff vs all other R

x = theFile[:,2]
y1 = theFile[:,1]
y2 = theFile[:,0]
y3 = theFile[:,3]
y4 = theFile[:,4]

plt.figure()
plt.subplot(111)
plt.xlabel('R_eff')
plt.ylabel('All other R')

plt.plot(x, y1, 'go', label="R_eff vs. R500")
plt.plot(x, y2, 'bo', label="R_eff vs. R200")
plt.plot(x, y3, 'ro', label="R_eff vs. R_half (3D)")
plt.plot(x, y4, 'co', label="R_eff vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('R_eff_allR.png', format='png')

#plot R_half (3D) vs all other R

x = theFile[:,3]
y1 = theFile[:,1]
y2 = theFile[:,2]
y3 = theFile[:,0]
y4 = theFile[:,4]

plt.figure()
plt.subplot(111)
plt.xlabel('R_half (3D)')
plt.ylabel('All other R')

plt.plot(x, y1, 'go', label="R_half (3D) vs. R500")
plt.plot(x, y2, 'bo', label="R_half (3D) vs. R_eff")
plt.plot(x, y3, 'ro', label="R_half (3D) vs. R200")
plt.plot(x, y4, 'co', label="R_half (3D) vs. R_half (faceon)")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('RH3D_allR.png', format='png')

#plot R_half (faceon) vs all other R

x = theFile[:,4]
y1 = theFile[:,1]
y2 = theFile[:,2]
y3 = theFile[:,3]
y4 = theFile[:,0]

plt.figure()
plt.subplot(111)
plt.xlabel('R_half (faceon)')
plt.ylabel('All other R')

plt.plot(x, y1, 'go', label="R_half (faceon) vs. R500")
plt.plot(x, y2, 'bo', label="R_half (faceon) vs. R_eff")
plt.plot(x, y3, 'ro', label="R_half (faceon) vs. R_half (3D)")
plt.plot(x, y4, 'co', label="R_half (faceon) vs. R200")
plt.xscale('log')
plt.yscale('log')

plt.legend(bbox_to_anchor=(1.5,0.5))
plt.show
plt.savefig('RHface_allR.png', format='png')
