import numpy as np
from scipy import interpolate

class Ocean():
    def _init_(self, c_fn, a_fn):
        c_tab = np.loadtxt(c_fn)
        a_tab = np.loadtxt(a_fn)
        self.c_spl = interpolate.splrep(*c_tab, s=0)
        self.a_spl = interpolate.bisplrep(*a_tab, s=0)

    def make_props(self, zs, freq=33300):
        a = interpolate.splev(zs, freq, self.a_spl)
        c = interpolate.bisplev(zs, freq, self.c_spl)
        return c, a