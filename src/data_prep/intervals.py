from sys import argv
from json import load

import numpy as np

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
            i_times = (raw_times[1:]+raw_times[:-1])/2
            ints = np.diff(raw_times)
            skips = np.diff(data[:, 0])
            ints /= skips
            slope, off = np.polyfit(i_times, ints, 1)
            print(src['name'], np.mean(ints), slope*1e3)


if __name__ == '__main__':
    main(argv)