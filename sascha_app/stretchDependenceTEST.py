# Name: Anthony Tracy
# Email: Anthony.Tracy@colorado.edu
# Description: This is a function that is basically a look up table. If the value is between two knowns, interpolate.
# NOTE: I am using a whitespace of 2 spaces.


import matplotlib.pyplot as plt
import numpy as np						# ONLY FOR THE SAKE OF TESTING LATER....


def interp2d(data,z,x):
  # Inputs:
  #  data - The known [(x1,y1),(x2,y2)]
  #  z -    The output of f(x,y) for each of the inputs in order of 11,12,21,22....
  #  x -    The (x,y) point to interpolate
  # f(x,y) = a0 + a1x + a2y + a3xy (approximatly)
  
  pnt1,pnt2=data        # pntN = (xN,yN) of known data.
  # The following is to make my life, and anyone who needs to read this, life's easier...
  # These bellow lines get called a lot so reduce number of multiplication calls...
  x1x2_y1y2 = (pnt1[0]-pnt2[0])*(pnt1[1]-pnt2[1])
  x1x2_y2y1 = (pnt1[0]-pnt2[0])*(pnt2[1]-pnt1[1])
  # The following coeffs came from solving a system of linear equations using boundaries of the known 4 points.
  a0 = (z[0]*pnt2[0]*pnt2[1])/x1x2_y1y2 \
  + (z[1]*pnt2[0]*pnt1[1])/x1x2_y2y1 \
  + (z[2]*pnt1[0]*pnt2[1])/x1x2_y2y1 \
  + (z[3]*pnt1[0]*pnt1[1])/x1x2_y1y2
  a1 = (z[0]*pnt2[1])/x1x2_y2y1 \
  + (z[1]*pnt1[1])/x1x2_y1y2 \
  + (z[2]*pnt2[1])/x1x2_y1y2 \
  + (z[3]*pnt1[1])/x1x2_y2y1
  a2 = (z[0]*pnt2[0])/x1x2_y2y1 \
  + (z[1]*pnt2[0])/x1x2_y1y2 \
  + (z[2]*pnt1[0])/x1x2_y1y2 \
  + (z[3]*pnt1[0])/x1x2_y2y1
  a3 = z[0]/x1x2_y1y2 \
  + z[1]/x1x2_y2y1 \
  + z[2]/x1x2_y2y1 \
  + z[3]/x1x2_y1y2

  return (a0+a1*x[0]+a2*x[1]+a3*x[0]*x[1])


def stretchDep(volt,impact):     # Incase it isn't clear, input is in units of Volts and mm's
  # This is just the hard coded data that will be used to interpolate the other possible input data points.
  # Make sure that the input is within the region of known data:
  assert(volt <= 2900 and volt >= 2500),"The input voltage is outside the known dataset. It must be between 2500 and 2900"
  assert(impact <= 104.2 and impact >= 53.8),"The input impact location is outside the known dataset. It must be between 52.8 and 104.2"
  volts = [2500,2500,2500,2600,2600,2600,\
	       2685,2685,2685,2700,2700,2700,\
	       2800,2800,2800,2900,2900,2900]
  locs  = [52.8,75.7,104.2,52.8,75.7,104.2,\
           52.8,75.7,104.2,52.8,75.7,104.2,\
           52.8,75.7,104.2,52.8,75.7,104.2]

  stretch = [950,908,883,888,856,826,837,815,788,837,769,740,796,769,740,759,734,707]
  mydict = {}

  #volt = round(volt)
  #impact = round(impact)

  for i in range(len(stretch)):
    mydict[(volts[i],locs[i])]=stretch[i]
  
  # If data is in the dictionary:
  if mydict.has_key((volt,impact)):
    return mydict[volt,impact]
  else:
    low = max([i if i < volt else 2500 for i in volts]),max([i if i < impact else 52.8 for i in locs])
    high = min([i if i > volt else 2900 for i in volts]),min([i if i > impact else 104.2 for i in locs])
    data = [low,high]
    z = [mydict[low],mydict[low[0],high[1]],mydict[high[0],low[1]],mydict[high]]
    return interp2d(data,z,(volt,impact))	# Currently zero for false, as I have yet to do this part...


# Testing the above function:
#pairs = ((2500,52.8),(2500,75.7),(2500,104.2),(2600,52.8),(2600,75.7),(2600,104.2),\
#           (2685,52.8),(2685,75.8),(2685,104.2),(2700,52.8),(2700,75.8),(2700,104.2),\
#           (2800,52.8),(2800,75.8),(2800,104.2),(2900,52.8),(2900,75.8),(2900,104.2))


vSpace = np.linspace(2500,2900,10)
xSpace = np.linspace(53.8,103.2,10)

ds2D = np.zeros((len(vSpace),len(xSpace)))


for i in range(len(vSpace)):
  for j in range(len(xSpace)):
    ds2D[i,j]=(stretchDep(vSpace[i],xSpace[j]))
    
V,X = np.meshgrid(vSpace,xSpace)
dv = (vSpace[1]-vSpace[0])/2.
dx = (xSpace[1]-xSpace[0])/2.
extent = [vSpace[0]-dv, vSpace[-1]+dv, xSpace[0]-dx, xSpace[-1]+dx]
im = plt.imshow(ds2D,extent=extent)
plt.xlabel('Volts')
plt.ylabel('Impact Distance (mm)')
plt.colorbar(im)
plt.savefig("fullRangeTest.jpg")
plt.show(im)

