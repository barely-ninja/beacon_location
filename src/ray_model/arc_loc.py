from sys import argv
from json import load
from math import pi, sin, sqrt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import splprep
from matplotlib.pyplot import show, plot, savefig, scatter
from ocean import Ocean
from rays import AcousticField

def get_tt_model(z_s, z_r, files):
    ocean = Ocean(files['c'], files['a'])
    z = np.linspace(z_s, z_r, 10)
    c, a = ocean.make_props(z_grid)
    rays = AcousticField(z,a,c)
    return [result['r'], result['tt'] for result in propagator]

def make_model_func(r0, alph, x0):
    def model_func(x):
        nonlocal r0, alph, x0
        mx = x-x0
        return (mx-r0*sin(alph))/sqrt(mx**2+r0**2-2*r0*mx*sin(alph))
    return np.vectorize(model_func)

def unpack(x):
    offsets = np.array([0, 0, 0])
    scales = np.array([1e5, pi/2, 1e6])
    return offsets+x*scales

def make_min_func(kn, unp):
    def err_func(x):
        nonlocal kn, unp
        model = make_model_func(*unp(x))
        err = model(kn[:, 0])-kn[:, 1]
        ss = err.dot(err)
        print(ss)
        return ss
    return err_func

def main(args):
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)
    
    get_tt_model(cfg['z_s'], cfg['z_r'], cfg['model_fn'])

    for curve in cfg['curves']:
        data = np.loadtxt(curve['arc'])
        vdt = curve['dt']*cfg['tow']
        data[:, 0] *= vdt
        data[:, 1] *= cfg['c_mean']/cfg['sampling']
        diff_data = np.diff(data, axis=0)
        mt = (data[:-1, 0]+data[1:, 0])/2
        dtdx = diff_data[:, 1]/diff_data[:, 0]
        inv_data = np.vstack((mt, dtdx)).T
        print(inv_data)
        #plot(inv_data[:,1])
        #show()
        if curve['type'] == "simple":
            min_func = make_min_func(inv_data, unpack)
            inits = (0,0,0)
            bnds = [(0, 1),(-1, 1),(-1, 1)]
            result = minimize(min_func, inits, bounds=bnds, method="L-BFGS-B", options={'eps':1e-4, 'maxiter':10})
            model = make_model_func(*unpack(result.x))
            plot(model(inv_data[:,0]))
            plot(inv_data[:,1])
            show()
        else:
            raise NotImplementedError


if __name__ == '__main__':
    main(argv)