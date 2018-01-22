# Name: Anthony Tracy
# Email: antr9811@colorado.edu

import numpy as np

# X / Y dimesnsions of the grid being made
dims=[4,3]
# Youngs Modulous and stress? <- forgot what the two values neeeded where but they are included in code...
params=[10.0,1.0]

# Total number of elements due to the grid
N = dims[0]*dims[1]-1
print range(N)

# Now to test writting to a file:
filename='test.txt'

file=open(filename,'w')
file.write("Elem# V1 V2 V3 Young's Stress\n")
# This loop is done so that only the wanted elements are made in the right hand rule pattern:
for i in range(N-dims[0]):
  if (i+1)%dims[0]:
    file.write('{0} {1} {2} {3} {4}\n'.format(i, i+1,i+dims[0],params[0],params[1]))
    file.write('{0} {1} {2} {3} {4}\n'.format(i+1, i+1+dims[0],i+dims[0],params[0],params[1]))
file.close()

