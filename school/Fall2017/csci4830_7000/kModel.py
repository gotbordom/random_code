#!/bin/usr/env/python

# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# Description:
#   This is just a script that will test a kinematic model of a 4 wheel car reading data from wheel encoders
# Assumptions:
#  1. 2D world      - so I am assuming only x/y axis, don't have any hills to scale at this point.
#  2. Kinematics    - currently just kinematics so no issues with slip, should be able to get exact soliutions
#  3. small time    - So I am assuming that I take a reading at very high frequency so any angle I will get is very small
#  4. wheel radius  - for now assuming all wheels to have same constant radius (no tire decay).
#  5. start angle   - Assuming origin (x=0,y=0,theta=0) is forward along the X-axis.
# -> removing  6. Center Mass   - CM is assumed to be in exact center, Length/2 and Width/2
# Questions to think about:
#  1. X,Y ... - Shouldn't X,Y just be the shift from the CM of car to the wheel in question without any theta shift?

import numpy as np
import matplotlib.pyplot
import argparse

def kMod(ticks,params):
  # Description:
  #   This is a model that will track the (x,y) points of a car given the ticks from wheel encoders on each wheel.
  #   the params were added for the angles of the car as well as the dimensions of the car.
  # Inputs:
  #   ticks  - array of the tic readings: (tA,tB,tC,tD)
  #   N      - Number of ticks per rotation of the wheels.
  #   params - dimensions of car and angles needed: (alpha,theta,l1,l2,w1,w2,r,N)
  #     NOTE: keeping l1,l2/w1,w2 seperate since I am not assuming center of mass of the car to be geometric center.
  #     alpha - angle of the driving wheels
  #     theta - current orientation of the car
  #     l1/l2 - l1 is distance from center mass (CM) of car to front of car, l2 is rear of car to CM
  #     w1/w2 - w1 is width of car from left to CM, and w2 is right to CM
  #     r     - radius of the wheels. <- for now assuming all are the same.
  #     N     - Number of ticks per rotation of the wheels.
  


  alpha,theta,l1,l2,w1,w2,r,N=params

  CA = np.array([-w1, l1,1])
  CB = np.array([ w2, l1,1])
  CC = np.array([-w1,-l2,1])
  CD = np.array([ w2,-l2,1])

  A = np.dot(R(ticks[0],params),CA)
  B = np.dot(R(ticks[1],params),CB)
  C = np.dot(R(ticks[2],params),CC)
  D = np.dot(R(ticks[3],params),CD)

  cm = 0.25*(A+B+C+D) 
  return cm

def R(tic,params):
  # Description:
  #   This is just a rotation matrix for rotating the car frame to the global frame.
  # Inputs:
  #   tic   - just a needed tic number for the translation of this perticular wheel
  #   params- same parameters as in kMod

  alpha,theta,l1,l2,w1,w2,r,N=params

  arc = 2*np.pi*r*(tic/N)

  # for the sake of speeding things up, I did make the small angle approx... so I should change all my 
  # sines and cosines to their approximates... later though.
  Gx = arc*np.sin(alpha)
  Gy = arc*np.cos(alpha)

  rot = np.array([[np.cos(theta),-np.sin(theta),Gx],
                  [np.sin(theta), np.cos(theta),Gy],
                  [0,0,1]])
  return rot


# Parameters
alpha=np.pi*0.5
theta=np.pi*0.5
l1,l2=[1.0,1.0]
w1,w2=[0.5,0.5]
r=0.1
N=10

params = [alpha,theta,l1,l2,w1,w2,r,N]
ticks = [10,10,10,10]

print "Test 1: ", kMod(ticks,params)

# Now to drive the car forward...
# Let's say I read data in at a constant time step:
# Allow the car to travel at a constant Velocity.. i.e const number of ticks read every second:
dt   = 0.1
time = np.arange(0,1.1,dt)
v    = 10                  # Ticks / per second
ticks= np.array([v,v,v,v]) # So just V * time = ticks

cm = [0,0,0]
print cm
for i in time:
  cm = kMod(ticks*i,params)
  print "Time: ",i,"Ticks: ",ticks[0]*i,"Pos: ", cm



