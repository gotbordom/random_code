# Name: Anthony Tracy
# Email: Antr9811@colorado.edu
# Description: Just writing a 2d interpolator using bilinear interpolation:
# NOTE: whitespace = 2 spaces


def interp2d(data,z,x):
  # Inputs:
  #  data -	The known [(x1,y1),(x1,y2),(x2,y1),(x1,y1)]
  #  z -	The output of f(x,y) for each of the inputs in order of 11,12,21,22....
  #  x -	The (x,y) point to interpolate
  # f(x,y) = a0 + a1x + a2y + a3xy (approximatly)
  
  pnt1,pnt2=data		# pntN = (xN,yN) of known data.
  # The following coeffs came from solving a system of linear equations using boundaries of the known 4 points.
  a0 = (z[0]*pnt2[0]*pnt2[1])/((pnt1[0]-pnt2[0])*(pnt1[1]-pnt2[1])) \
  + (z[1]*pnt2[0]*pnt1[1])/((pnt1[0]-pnt2[0])*(pnt2[1]-pnt1[1])) \
  + (z[2]*pnt1[0]*pnt2[1]





