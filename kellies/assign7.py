#!bin/usr/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import sdss

# Load spectra:
	# Pull wavelen and flux from dict and Title
		# Convert wavelength
	# Get RGB Value for THIS wavelength and flux
	# Plot the wavelength vs flux in the RGB Color using title.

# Notes: My spacing is 2 spaces (nnot tabs)

loops = 12




for i in loops:
  # get full dataset:
  db = sdss.fakeSDSS()
  # Get wavelength and flux data:
  wave = np.array(db['wavelengths']./10.])		# This includes converting and using float notation
  flux = np.array(db['flux'])
  # Get title:
  
  
