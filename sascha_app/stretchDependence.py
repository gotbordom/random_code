# Name: Anthony Tracy
# Email: Anthony.Tracy@colorado.edu
# Description: This is a function that is basically a look up table. If the value is between two knowns, interpolate.
# NOTE: I am using a whitespace of 2 spaces.


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
  volts = [2500,2500,2500,2600,2600,2600,\
	       2685,2685,2685,2700,2700,2700,\
	       2800,2800,2800,2900,2900,2900]
  locs  = [52.8,75.7,104.2,52.8,75.7,104.2,\
           52.8,75.8,104.2,52.8,75.8,104.2,\
           52.8,75.8,104.2,52.8,75.8,104.2]

  stretch = [950,908,883,888,856,826,837,815,788,837,769,740,796,769,740,759,734,707]
  mydict = {}
  for i in range(len(stretch)):
    mydict[(volts[i],locs[i])]=stretch[i]
  
  # If data is in the dictionary:
  if mydict[volt,impact]:
    return mydict[volt,impact]
  # If data needs to be interpolated:
  else:
    low = max([i for i in volts if i < volts]),max([i for i in volts if i < impact])
    high = min([i for i in volts if i > volts]),min([i for i in volts if i > impact])
    
    return 0	# Currently zero for false, as I have yet to do this part...

# Testing the above function:
#pairs = ((2500,52.8),(2500,75.7),(2500,104.2),(2600,52.8),(2600,75.7),(2600,104.2),\
#           (2685,52.8),(2685,75.8),(2685,104.2),(2700,52.8),(2700,75.8),(2700,104.2),\
#           (2800,52.8),(2800,75.8),(2800,104.2),(2900,52.8),(2900,75.8),(2900,104.2))



print stretchDep(2600,52.8)

