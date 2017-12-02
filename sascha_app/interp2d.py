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

  return a0+a1*x+a2*y+a3*x*y

