#create FITs files from numpy arrays containing compiled powderday images in different wavelengths

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


