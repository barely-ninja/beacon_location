from sys import argv
from json import load
from math import pi, sin, sqrt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import splrep, splev
from matplotlib.pyplot import show, plot, savefig, ylim
from ocean import Ocean
from rays import AcousticField

def get_tt_model(z_s, z_r, files):
    ocean = Ocean(files['c'], files['a'])
    z = np.linspace(z_s, z_r, 10)
    params = [(z[i], *ocean.evaluate(z[i], 33.3)) for i in range(len(z))]
    rays = AcousticField(params)
    result = np.array([x for x in rays])
    spl = splrep(*result.T)
    base = np.linspace(result[0,0], result[-1,0], 20)
    dtdx = splev(base, spl, der=1)
    #plot(base,dtdx)
    #show()
    return spl

def make_model_func(rs, t0, v, spl):
    def model_func(t):
        nonlocal rs, t0, v, spl
        x = v*(t - t0)
        r = sqrt(rs**2+x**2)
        dtt = splev(r, spl, der=1)
        return dtt*v*x/r
    return np.vectorize(model_func)

def unpack(x):
    offsets = np.array([0, 0, 0])
    scales = np.array([1e5, pi/2, 1e6])
    return offsets+x*scales

def make_min_func(kn, v):
    def err_func(x):
        nonlocal kn, v
        ss = 0
        for i in range(len(kn)):
            rs = x[0]
            t0 = x[i+1]-kn[i]['t0']
            spl = kn[i]['spl']
            model = make_model_func(rs, t0, v, spl)
            err = model(kn[i]['t'])-kn[i]['di']
            #print(err)
            ss += err.dot(err)
        print(x)
        return ss
    return err_func

def main(args):
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)

    data_list = []
    inits = [1e3]
    bnds = [(0, 1e4)]

    for curve in cfg['curves']:
        tt_spl = get_tt_model(cfg['z_s'], curve['z_r'], cfg['model_fn'])

        data = np.loadtxt(curve['arc'])
        vdt = curve['dt']
        raw_times = data[:, 0]*curve['dt']+data[:, 1]/cfg['sampling']
        i_times = (raw_times[1:]+raw_times[:-1])/2
        ints = np.diff(raw_times)
        ints /= np.floor(ints)

        i_spl = splrep(i_times, ints, w=np.ones(len(ints)))
        base = np.linspace(i_times[0], i_times[-1], 10)
        dint_i = splev(base, i_spl, der=1)

        data_list.append({'t':base, 'di':dint_i, 'spl':tt_spl, 't0':curve['t_off']})

        inits.append(0)
        bnds.append((-1e4, 1e4))

    min_func = make_min_func(data_list, cfg['tow'])
    result = minimize(min_func, inits, bounds=bnds, method="L-BFGS-B", options={'eps':1e-1, 'maxiter':10})
    print(result.x)
    #model = make_model_func(*unpack(result.x))
    #plot(model(inv_data[:,0]))
    #plot(inv_data[:,1])
    #show()'''



if __name__ == '__main__':
    main(argv)