import numpy as np
from matplotlib import pyplot
pyplot.style.use('ggplot')
from mpl_toolkits.mplot3d import Axes3D



class impact:
    def __init__(self,name):
        self.name = name
        self.data = {}     # Since there is data for f(x) and g(x) top and bottom functions
        self.coeffs = {}   # There will be coeffs for each function as well
        self.n = 0
    def add_data(self,x,f_x,g_x):
        self.data['f_x'] = f_x
        self.data['g_x'] = g_x
        self.data['x'] = x
        
    def get_coeffs(self,n):
        # Notes:
        #    x : The x input for a given f(x)
        #    y : The measured results of the x values
        #    n : n-1 is the heighest order of the cheby Shev polynomials to be used

        x = self.data['x']
        # Normalize x to be within range [-1,1]
        xNorm = (x/(0.5*max(x)))-1
        print(xNorm[0],xNorm[-1])
        self.n = n
        self.coeffs['f_x'] = np.polynomial.chebyshev.chebfit(xNorm,self.data['f_x'],deg=n)
        self.coeffs['g_x'] = np.polynomial.chebyshev.chebfit(xNorm,self.data['g_x'],deg=n)
    
    def visualize_3D(self,x,y): #coeffs,rad_sym=True):#,vander=vander_chebyshev):
        # Notes:
        #    x/y    : The coordiantes for a meshgrid, that the impact will be interpolated over
    
        # NOTE: I don't need to tell this method the number of dimensions to approximate with:
        #     Reason 1: I could just use len(coeffs)
        #     Reason 2: I would only need it for solving the matrix,
        #               but python uses it's own method that just uses len(coeffs).

        # Create meshgrids for x,y,r:
        xx, yy = np.meshgrid(x,y)
        rr = np.sqrt(xx*xx+yy*yy)

        # Just to make this more readable later on in life:
        coeffs_top = self.coeffs['f_x']
        coeffs_bot = self.coeffs['g_x']

        # Make sure all values of rr are withing range [0,1] - since we are using polynomials
        rr[rr>1] = 1
        # Make it a decent input for the vander_chebyshev method
        rr_ = rr.flatten()

        zTop = np.polynomial.chebyshev.chebval(rr_,coeffs_top)
        zTop = zTop.reshape(np.shape(rr))

        zBot = np.polynomial.chebyshev.chebval(rr_,coeffs_bot)
        zBot = zBot.reshape(np.shape(rr))

        print(np.shape(zTop),np.shape(zBot))

        # Now plot visuals in 3D:
        fig = pyplot.figure()
        
        axes = fig.add_subplot(111,projection='3d')
        axes.plot_surface(xx, yy, zTop, cmap=pyplot.get_cmap());
        axes.plot_surface(xx, yy, zBot, cmap=pyplot.get_cmap());
        
        axes.set_xlabel("x label") 
        axes.set_ylabel("y label")
        axes.set_zlabel("z label")

        pyplot.show()






# Testing the class:

# Measurements 2:
f2 = np.array([47.1,47.07,47.25,48.12,
      59.04,45.91,14.6,-2.97,
      -9.24,-6.07,2.51,16.51,
      52.26,53.42,48.14,47.14,
      46.76,46.76,46.76,46.76])
g2 = np.array([0,0,0,0,-1.91,-5.98,
      -11.78,-20.97,-26.24,
      -24.02,-19.07,-10.57,
      -3.58,-1.19,0,0,0,0,0,0])
x2 = np.array([0,1.3,5.17,11.5,20.13,
      31.85,43.47,57.1,72.22,
      87.64,103.36,118.19,133.74,
      147.5,160.24,170.05,179.55,
      185.49,189.05,191])



xSpace = np.linspace(-1.5,1.5,41)

print(len(x2),len(g2))

c1 = impact("cX18")
c1.add_data(x2,f2,g2)
c1.get_coeffs(18)
c1.visualize_3D(xSpace,xSpace)

