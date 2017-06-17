import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import C2K
from scipy import interpolate

def in_ipynb():
    try:
        cfg = get_ipython().config 
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return True
        else:
            return False
    except NameError:
        return False

if in_ipynb():
    from plotly.offline import init_notebook_mode, plot, iplot
    import plotly.tools as tls
    init_notebook_mode(connected=True)

class coolingPath:
    """ Define a cooling path, Time is input in Myr BP
    """
    def __init__(self, t, T):
        t = np.array(t)
        self.t = np.abs(t-t.max())
        self.TC = np.array(T)
        self.TK = C2K(T)
        self.tf = self.t[-1]

        self.TMAX = self.TK.max()
        self.TMIN = self.TK.min()
        self.dT = self.TMAX - self.TMIN

        # The heating history is represented by pairs (time,temperature). A
        # temperature of 0 is the hottest and 1 is coldest. The temperature
        # is piecewise linear in between
        self.NDT = 1.0 - (self.TK - self.TMIN) / self.dT
    
        self.getTemp = interpolate.interp1d(self.t, self.NDT,
                                            bounds_error=False,
                                            fill_value = (self.NDT[0], self.NDT[-1]))

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim((self.t.min(), self.t.max()))
        ax.set_ylim((130., 0.))
        ax.plot(self.t,self.TC)
        ax.set_title("Cooling Path")
        ax.set_xlabel("Time (Myr)")
        ax.set_ylabel("Temperature")
        if in_ipynb():
            plotly_fig = tls.mpl_to_plotly(fig)
            iplot(plotly_fig)
        else:
            plt.show()
        return ax
        

wolf1 = coolingPath((100.0,44.0,43.0,0.0), (130.0,130.0,10.0,10.0)) 
wolf2 = coolingPath((100.0,0.0), (130.0,10.0))
wolf3 = coolingPath((100.0,19.5,19.0,0.0), (60.0,60.0,10.0,10.0))
wolf4 = coolingPath((100.0,76.0,24.0,0.0), (100.0,60.0,60.0,10.0))
wolf5 = coolingPath((100.0, 5.0, 0.0), (18.0, 64.0, 10.0))
