# Name: Anthony Tracy
# Email: Anthony.Tracy@colorado.edu
# Description: This is a function that is basically a look up table. If the value is between two knowns, interpolate.
# NOTE: I am using a whitespace of 2 spaces.


def interp2D(pairs,z,x,y):
  # This is given a pair of points to interpolate, my aim is to just linearly interpolate. Very simple approach.
  # pairs: 	The dictionary used here, or in other cases a set of tuples (x,y)
  # z: 		The known stretch terms, or a 3rd dimension if used in other cases
  # x,y:	These should be the input that needs to be interpolated. y is the Volts, x is the crater location
 
  # Find the bounding tuples I need to interpolate:
  # let y1/x1 & y2/x2 be upper & lower voltage/Impact Loc bounds
  
  # Now interpolate...
  

  return 0 # for now it does nothing so it returns 0 but doesn't cause an error in my code...

def stretchDep(volt,impact):     # Incase it isn't clear, input is in units of Volts and mm's
  # This is just the hard coded data that will be used to interpolate the other possible input data points.
  pairs = ((2500,52.8),(2500,75.7),(2500,104.2),(2600,52.8),(2600,75.7),(2600,104.2),\
	   (2685,52.8),(2685,75.8),(2685,104.2),(2700,52.8),(2700,75.8),(2700,104.2),\
	   (2800,52.8),(2800,75.8),(2800,104.2),(2900,52.8),(2900,75.8),(2900,104.2))
  stretch = (950,908,883,888,856,826,837,815,788,837,769,740,796,769,740,759,734,707)
  mydict = {}
  for i in range(len(stretch)):
    mydict[pairs[i]]=stretch[i]
  
  # If data is in the dictionary:
  if mydict[volt,impact]:
    return mydict[volt,impact]
  # If data needs to be interpolated:
  else:
    return 0	# Currently zero for false, as I have yet to do this part...

# Testing the above function:
# So the following matches the paper I have been given. Great, I made a look-ip table, now to make the interpolate portion...

pairs = ((2500,52.8),(2500,75.7),(2500,104.2),(2600,52.8),(2600,75.7),(2600,104.2),\
           (2685,52.8),(2685,75.8),(2685,104.2),(2700,52.8),(2700,75.8),(2700,104.2),\
           (2800,52.8),(2800,75.8),(2800,104.2),(2900,52.8),(2900,75.8),(2900,104.2))

for i in pairs:
  print stretchDep(i[0],i[1])


