#!/bin/usr/env/python

# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# Description:
#   This is just a script that will test a kinematic model of a 4 wheel car reading data from wheel encoders
# Assumptions:
#  1. 2D world	    - so I am assuming only x/y axis, don't have any hills to scale at this point.
#  2. Kinematics    - currently just kinematics so no issues with slip, should be able to get exact soliutions
#  3. small time    - So I am assuming that I take a reading at very high frequency so any angle I will get is very small
#  4. wheel radius  - for now assuming all wheels to have same constant radius (no tire decay).
#  5. start angle   - Assuming origin (x=0,y=0,theta=0) is forward along the X-axis.
#  6. Center Mass   - CM is assumed to be in exact center, Length/2 and Width/2
# Questions to think about:
#  1. X,Y ... - Shouldn't X,Y just be the shift from the CM of car to the wheel in question without any theta shift?


import numpy as np
import matplotlib.pyplot as plt
import argparse


def kModel1(start,tics,params):
  # Description:
  #   This is a kinetic model of a simplified car. It will be assumed that it is in a 2D worls so it will only rotate
  #   about the z-axis:
  # Inputs:
  #   start- [[xA,yA,alpha],	These are the x,y-coords of each wheel and their angles (from their reference frame)
  #           [xB,xB,beta],
  #           [xC,xC,gamma],
  #           [xD,yD,delta]]
  #   tics  - will be all the tics read from the wheel encoders for all wheels
  #   params- (W,L,theta,R,N) - Width of car(X-axis), length of car (Y-axis), theta=0 car points forward along Y-axis
  pntA,pntB,pntC,pntD=start
  # Each wheel will have slightly different params because X,Y are physical distances from the CM of car.
  W,L,theta,R,N=params
  
  Agf=rot(pntA,tics[0],[0.5*W,0.5*L,theta,R,N])   # Front left wheel  -> global frame
  Bgf=rot(pntB,tics[1],[0.5*W,-0.5*L,theta,R,N])  # Front right wheel -> " "
  Cgf=rot(pntC,tics[2],[-0.5*W,-0.5*L,theta,R,N]) # Rear right wheel  -> " "
  Dgf=rot(pntD,tics[3],[-0.5*W,0.5*L,theta,R,N])  # Rear left wheel   -> " "

  return np.array([Agf,Bgf,Cgf,Dgf])


def rot(pnt,tics,params):
  # Description: 
  #   This is a helper rotation matrix to shift the pnt of the wheel (in it's reference frame) to the global frame (gf)
  # Inputs:
  #   pnt
  #   tics
  #   params- (X,Y,theta,R,N) - note angles (theta) need to be in radians....
   
  # Pull out angle and re-write it to be a 1 for matrix math...
  alpha = pnt[2]
  pnt[2] = 1
  X,Y,theta,R,N,=params

  #print alpha
  #print pnt
  #print params

  # Now to get Tx,Ty:
  arc = 2*np.pi*R*(tics/N)
  Tx = arc*np.sin(alpha)
  Ty = arc*np.cos(alpha)

  #print arc, Tx, Ty

  # Rotate from wheel frame to global frame:
  rotM = np.array([[np.cos((alpha+theta)),-1*np.sin((alpha+theta)),X*np.cos(alpha)-Y*np.sin(alpha)+Tx],
                   [np.sin((alpha+theta)),np.cos((alpha+theta)),X*np.sin(alpha)+Y*np.cos(alpha)+Ty],
                   [0,0,alpha]])
  pntGF = np.dot(rotM,pnt)
  
  #print rotM
  #print pntGF
  
  return pntGF

# Testing Full kModel1:

# Test1: Let all wheels start at their origins. Theta = alpha = 0 : Car goes forward along Y-axis:
#   Test1 - seems to be working.
# Test2: Let theta = alpha = pi/2 so car goes forward along X-axis
#   Test2 - Seems fine
# Test3: let theta = alpha = pi - should go down (- Y-axis)
#   Test3 - seems fine
# Test4: let theta = alpha = -pi/2 - should go forward on neg X-axis
start=np.array([[0,0,-0.5*np.pi],    #   start    - [[xA, yA, alpha],
                [0,0,-0.5*np.pi],    #               [xB, xB, beta ],
                [0,0,-0.5*np.pi],    #               [xC, xC, gamma],
                [0,0,-0.5*np.pi]])   #               [xD, yD, delta]]
ticks=[100,100,100,100]
params=[1.0,2.0,-0.5*np.pi,1.0,100] # (W,L,theta,R,N)

pntsGF=kModel1(start,ticks,params)

print pntsGF
print pntsGF[:,:2]

plt.scatter(pntsGF[:,0],pntsGF[:,1])
plt.show()

