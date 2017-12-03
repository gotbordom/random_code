# Name: Anthony Tracy
# Email: Antr9811@colorado.edu
# Description: Just writing a 2d interpolator using bilinear interpolation:
# NOTE: whitespace = 2 spaces


def interp2d(data,z,x):
  # Inputs:
  #  data -	The known [(x1,y1),(x2,y2)]
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
  
  return (a0+a1*x[0]+a2*x[1]+a3*x[0]*x[1])


# Testing:
data = [(2600,52.8),(2685,75.7)]
z = [888.0,856.0,837,815]	# [f(v1,x1),f(v1,x2),f(v2,x1),f(v2,x2)]
x = [2650,60]

print data
print z
print x

test = interp2d(data,z,x)

print test

