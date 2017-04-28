from sys import argv
from json import load

import numpy as np
from scipy.optimize import curve_fit


def expon(t, i0, t0):
    return i0+np.exp(5.5e-5*(t-t0))


def main(args):
 
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)
    times = [x['time'] for x in cfg['curves']]
    ints = []
    for src in cfg['curves']:
        data = np.loadtxt(src['picks'])
        raw_times = data[:, 0]*src['dt']+data[:, 1]/cfg['sampling']
        int0, _ = np.polyfit(data[:,0], raw_times, 1)
        ints.append(int0)

    popt, pcov = curve_fit(expon, times, ints)

    print(popt, popt[1]/86400)


if __name__ == '__main__':
    main(argv)