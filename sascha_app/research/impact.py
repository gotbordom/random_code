import numpy as np
from matplotlib import pyplot
pyplot.style.use('ggplot')
from mpl_toolkits.mplot3d import Axes3D



class impact:
    def __init__(self,name,center=0,pix2um=1):
        self.name = name
        self.data = {}     # Since there is data for f(x) and g(x) top and bottom functions
        self.coeffs = {}   # There will be coeffs for each function as well
        self.n = 0
        self.volume = 0
        self.center = center # Want to know if impact is actually centered at 0 or other
        # NOTE: I should eventually change this so that I use a numerical method to find lowest point of my fit function
        self.pix2um=pix2um

    def add_data(self,x,f_x,g_x):
        self.data['f_x'] = f_x
        self.data['g_x'] = g_x
        self.data['x'] = x

    def convert_pix2um(self):
        self.data['x'] = self.data['x']/self.pix2um
        self.data['f_x'] = self.data['f_x']/(self.pix2um*0.788) # 0.788 approx sin(52 degrees)
        self.data['g_x'] = self.data['g_x']/(self.pix2um*0.788)
        
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

   
    def interp_data(self,r):
        # Notes:
        #    r : Radial data to interpolate on
        if(self.center != 0): r+=self.center        
        self.data['r_pred'] = r
        self.data['f_r_pred'] = np.polynomial.chebyshev.chebval(r,self.coeffs['f_x'])
        self.data['g_r_pred'] = np.polynomial.chebyshev.chebval(r,self.coeffs['g_x'])

    def integrate(self):
        diff = self.data['f_r_pred']-self.data['g_r_pred']
        diff_radial = np.multiply(self.data['r_pred']-self.data['r_pred'][0],diff)
        true_vol = np.pi*diff[-1]*(self.data['r_pred'][-1]-self.data['r_pred'][0])**2
        pred_vol = 2*np.pi*np.trapz(diff_radial,self.data['r_pred'])
        print('{0}/{1} = {2}'.format(pred_vol,true_vol,pred_vol/true_vol))

    def visualize_2D(self,f_x='True',g_x='True'):
        # Plotting just the data:
        x = self.data['x'] / (0.5*max(self.data['x']))
        x -= 1
        print(x)
        if f_x:
            pyplot.plot(x,self.data['f_x'],'r')
            pyplot.plot(self.data['r_pred'],self.data['f_r_pred'],'b--')
        if g_x:
            pyplot.plot(x,self.data['g_x'],'r')
            pyplot.plot(self.data['r_pred'],self.data['g_r_pred'],'b--')

    def visualize_3D(self,rad,n): #,off_center=0): #coeffs,rad_sym=True):#,vander=vander_chebyshev):
        # Notes:
        #   off_center : This is just used encase  the center of impact is not actually zero this shifts to zero
        #   rad        : This is the radius of the volume to be visualized    
        #   n          : number of ticks in the radius - so 10 means a 10,10 meshgrid

        # NOTE: I don't need to tell this method the number of dimensions to approximate with:
        #     Reason 1: I could just use len(coeffs)
        #     Reason 2: I would only need it for solving the matrix,
        #               but python uses it's own method that just uses len(coeffs).

        # Create meshgrids for x,y,r:
        rSpace = np.linspace(-rad,rad,n)
        xx, yy = np.meshgrid(rSpace,rSpace)
        rr = np.sqrt(xx*xx+yy*yy)
        rr += self.center
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
        
        pyplot.title(self.name)
        #axes.set_xlabel("length of crater in x (um)") 
        axes.set_ylabel("length of crater in y (um)")
        axes.set_zlabel("Ir coating of 1/4 um")

        pyplot.show()






# Testing the class:

# Measurements 2:
x18_c1_f2 = np.array([47.1,47.07,47.25,48.12,
      59.04,45.91,14.6,-2.97,
      -9.24,-6.07,2.51,16.51,
      52.26,53.42,48.14,47.14,
      46.76,46.76,46.76,46.76])
x18_c1_g2 = np.array([0,0,0,0,-1.91,-5.98,
      -11.78,-20.97,-26.24,
      -24.02,-19.07,-10.57,
      -3.58,-1.19,0,0,0,0,0,0])
x18_c1_x2 = np.array([0,1.3,5.17,11.5,20.13,
      31.85,43.47,57.1,72.22,
      87.64,103.36,118.19,133.74,
      147.5,160.24,170.05,179.55,
      185.49,189.05,191])

# X18_c10 measurements:
x18_c10_f = np.array([43.86,43.88,43.89,43.97,47.24,48.16,55.8,30.19,12.97,7.87,13.79,28.6,53.36,44.62,43.79,42.71,42.47,42.62,42.75,42.62])
x18_c10_g = np.array([0,0,0,0,0,0,-2.5,-5.25,-8.75,-10.49,-7.03,-2.5,-1.36,0,0,0,0,0,0,0])
x18_c10_x = np.array([0,1.3,5.17,11.5,20.19,31.85,43.47,57.1,72.22,87.64,103.36,118.15,133.74,147.5,160.26,170.08,179.64,185.51,189.08,191])


x18_c2_f=np.array([74,77.43,86.1,88.5,85.75,83.25,109.5,108.5,102.26,-28,-39,-31,65.44,0,-71.76,-88.76,-66.52,-23.25,55.75,109.01,72.52,72.52,66.5,68.26,66.75,68.52,65.52])
x18_c2_g=np.array([0,0,0,0,0,0,0,6.25,-30.51,-45.25,-118.75,-129.75,-137.09,-139.51,-133.76,-129.76,-114.52,-56.27,-26,-5.51,9.26,0,0,0,0,0,0])
x18_c2_x=np.array([0,19.35,39.92,63.61,95.09,120.67,174.94,189.07,226.66,251.2,293.7,327.46,345.04,359.32,376.65,397.06,418.77,457.7,483.49,504.31,528.8,575.61,619.64,642.52,664.4,701.15,722.7])



#xSpace = np.linspace(-1.5,1.5,101)

#xx,yy = np.meshgrid(xSpace,xSpace)
#rr = np.sqrt(xx*xx+yy*yy)

# C1_rr need to be scaled back to 0:
#rr_c1 = rr-0.22

# x18 crater1
x18_c1 = impact("cX18",center=-0.22,pix2um=201)
x18_c1.add_data(x18_c1_x2,x18_c1_f2,x18_c1_g2)
x18_c1.convert_pix2um()
x18_c1.get_coeffs(18)
x18_c1.interp_data(np.linspace(-0.22,1,201))
x18_c1.integrate()


x18_c1.visualize_3D(1.5,101) #,-0.22)


# x18 crater 10:
x18_c10 = impact("x18_c10",center=-0.05,pix2um=201)
x18_c10.add_data(x18_c10_x,x18_c10_f,x18_c10_g)
x18_c10.convert_pix2um()
x18_c10.get_coeffs(18)
x18_c10.interp_data(np.linspace(0,1,201))
x18_c10.integrate()


x18_c10.visualize_3D(1.5,101)

# x18 crater 2:
#x18_c2 = impact("x18_c2",0.5)
#x18_c2.add_data(x18_c2_x,x18_c2_f,x18_c2_g)
#x18_c2.get_coeffs(18)
#x18_c2.interp_data(np.linspace(0,1,201))
#x18_c2.integrate()

#x18_c2.visualize_3D(1.5,101)

