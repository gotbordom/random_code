#!/usr/bin/env python

# MAKE SURE TO CHANGE THE ABOVE IF YOU USE A DIFF PATH

# Name: Anthony
# Description: Intrested in Kellie's assignment. She's cure...
# 

# Notes: Whitespace = 2 spaces... Spaces are better than tabs!!!! 

import numpy as np
import matplotlib.pyplot as plt
import argparse

def B(lam,T):
  # Note that:
	# lam is lambda, the wavelength	  - Units: m
	# T is tempurature.				  - Units: K
  h = 6.6e-34	# Plank's contant	  - Units: J/s
  c = 3.0e+8	# Speed of light	  - Units: m/s
  K = 1.4e-23	# Boltzmann constant  - Units: J/K
  b = np.exp((h*c)/(lam*K*T))

  # Note to self: I wonder if lam**5 would end up taking less operations that lam*lam*lam... <- it does for low power
  return (2*h*c*c)/(lam**5*(b-1))

def test_(t,H,f):
  # Note that:
	# f is frequency.	- Units: 1/s
  test_p = np.sin((2*np.pi*f*t/len(t))+H)
  test_m = np.sin((2*np.pi*f*t/len(t))-H)
  return (test_p-test_m)/(2*H)

# Note that in my notation B is a function and B_ is the derivative where '_' replaces the prime following a function

def B_(lam,H,T):
  # Note that:
	# lam is again lambda from function B
	# H is this is the derivative step used.
  Bp = B(lam+H,T)	# Just seperating everything out in case of a need for debugging
  Bm = B(lam-H,T)	# ^...
  return (Bp-Bm)/(2*H)

# Now to test these functions:
lam = np.arange(1,100)*1e-7	#	- Units: m
T = 5800	# This is temp 		- Units: Kelvin
H = 0.01e-7	# derivative step	- No units
f = 1		# Frequency of test	- Units: 1/s
# H Needs to be on the same scale as lam...

time = np.arange(1,100)		#	- Units: s...

# making ds for dataset and dataset'
ds = []
ds_ = []

# Making sure the code works as expected:
dt = np.sin(2*np.pi*f*time/len(time))
dt_ = test_(time,H,f)

print dt

# Create the data for each function:
for i in lam:
  ds.append(B(i,T))
  ds_.append(B_(i,H,T))

# Plot the data:
f,ax = plt.subplots(3)
ax[0].plot(lam,ds,'g')
ax[0].set_title("The main function B")

ax[1].plot(lam,ds_,'k')
ax[1].set_title("The derivative of B")

ax[2].plot(time,dt,'g',time,dt_,'k')
ax[2].set_title("Testing data with Sine and derivative")

plt.show()
