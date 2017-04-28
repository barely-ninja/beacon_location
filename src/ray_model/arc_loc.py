from sys import argv
from json import load
from math import pi, sin, sqrt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import splrep, splev
from matplotlib.pyplot import show, plot, savefig, ylim, close
from ocean import Ocean
from rays import AcousticField

def get_tt_model(z_s, z_r, files):
    ocean = Ocean(files['c'], files['a'])
    z = np.linspace(z_s, z_r, 10)
    params = [(z[i], *ocean.evaluate(z[i], 33.3)) for i in range(len(z))]
    rays = AcousticField(params)
    result = np.array(list(rays))
    spl = splrep(*result.T)
    base = np.linspace(result[0,0], result[-1,0], 20)
    d2tdx2 = splev(base, spl, der=2)
    plot(base, d2tdx2)
    show()
    return spl

def make_model_func(rs, t0, v, spl):
    def model_func(t):
        nonlocal rs, t0, v, spl
        x = v*(t - t0)
        r = sqrt(rs**2+x**2)
        dtt = splev(r, spl, der=2)
        return dtt*v*x/r
    return np.vectorize(model_func)

def make_min_func(kn, v):
    def err_func(x):
        nonlocal kn, v
        ss = 0
        for i in range(len(kn)):
            rs = x[0]
            t0 = x[1]-kn[i]['t0']
            spl = kn[i]['spl']
            model = make_model_func(rs, t0, v, spl)
            err = model(kn[i]['t'])-kn[i]['di']
            #print(err)
            ss += err.dot(err)
        #print(ss)
        return ss*1e8
    return err_func

def main(args):
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)

    data_list = []
    inits = [1e3, 0]
    bnds = [(0, 1e4), (-1e4, 1e4)]

    for curve in cfg['curves']:
        tt_spl = get_tt_model(cfg['z_s'], curve['z_r'], cfg['model_fn'])


    '''data_list.append({'t':base, 'di':dint_i, 'spl':tt_spl, 't0':curve['t_off']})

    min_func = make_min_func(data_list, cfg['tow'])
    result = minimize(min_func, inits, bounds=bnds, method="L-BFGS-B", options={'eps':1e2})
    print(result.x)
    for i in range(len(data_list)):
        v = cfg['tow']
        rs = result.x[0]
        t0 = result.x[1]-data_list[i]['t0']
        print(-v*t0, sqrt(rs**2+(v*t0)**2))
        spl = data_list[i]['spl']
        model = make_model_func(rs, t0, v, spl)
        plot(data_list[i]['t'], model(data_list[i]['t']))
        plot(data_list[i]['t'], data_list[i]['di'])
        ylim((0, 1/1500))
        #savefig(cfg['curves'][i]['name']+'.png')
        #close()
        show()'''


if __name__ == '__main__':
    main(argv)