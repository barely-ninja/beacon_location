import numpy as np
from scipy import interpolate

class Ocean():
    def __init__(self, c_fn, a_fn):
        c_tab = np.loadtxt(c_fn)
        a_tab = np.loadtxt(a_fn)
        self.c_spl = interpolate.splrep(*c_tab.T, w=np.ones_like(c_tab[:,0]))
        self.a_spl = interpolate.bisplrep(*a_tab.T, w=np.ones_like(a_tab[:,0]))

    def evaluate(self, zs, freq):
        c = interpolate.splev(zs, self.c_spl)
        a = interpolate.bisplev(zs, freq, self.a_spl)
        return np.asscalar(c), a*1e-3