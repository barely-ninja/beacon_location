from sys import argv
from json import load
from math import exp
import numpy as np
from scipy.optimize import curve_fit

def make_parab(b):
    def parabolic(x, a, c):
        nonlocal b
        return a*x*x+b*x+c
    return parabolic

def main(args):
 
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)

    for wave in cfg:
        print(wave['wave_name'])
        for src in wave['files']:
            data = np.loadtxt(src['picks'])
            raw_times = data[:, 0]*src['dt']+data[:, 1]/44100.0
            int0 = wave['drift'][0]+exp(wave['drift'][1]*(src['time']-wave['drift'][2]))
            parab = make_parab(int0)
            popt, pcov = curve_fit(parab, data[:,0], raw_times)
            result = popt[0]/(src['dt']**2)
            print(src['name'], result)


if __name__ == '__main__':
    main(argv)