from sys import argv
from json import load

from math import pi, sin, sqrt
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import splrep, splev
from matplotlib.pyplot import show, plot, savefig, close

def parse_time(time_string):
    hours, mins =  [int(x) for x in time_string.split('-')]
    return 3600*hours+60*mins


def main(args):
 
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)

    data_list = []

    for curve in cfg['curves']:

        t1 = parse_time(curve['t_det'])
        t2 = t1+parse_time(curve['t_len'])

        data = np.loadtxt(curve['picks'])
        raw_times = data[:, 0]*curve['dt']+data[:, 1]/cfg['sampling']
        i_times = (raw_times[1:]+raw_times[:-1])/2
        ints = np.diff(raw_times)
        ints /= np.floor(ints)
        print(t1, t2, np.mean(ints))

        '''i_spl = splrep(i_times, ints, w=np.ones(len(ints)))
        base = np.linspace(i_times[0], i_times[-1], 10)
        d2int_i = splev(base, i_spl, der=1)
        int_i = splev(base, i_spl)
        plot(d2int_i, int_i)
        show()'''
        #data_list.append({'t':base, 'd2i':dint_i, 'spl':tt_spl, 't0':curve['t_off']})

    '''min_func = make_min_func(data_list, cfg['tow'])
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