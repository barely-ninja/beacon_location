from sys import argv
from json import load
from collections import namedtuple
from math import log, exp
import numpy as np

from matplotlib.pyplot import show, plot, savefig, close

def parse_time(time_string):
    hours, mins =  [int(x) for x in time_string.split('-')]
    return 3600*hours+60*mins

Interval = namedtuple('Interval', 't1 t2 int')

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
        data_list.append(Interval(t1, t2, log(np.mean(ints)-1)))
    sort_data = sorted(data_list, key=lambda x: x.int)

    int1 = (sort_data[1].int+sort_data[2].int)/2
    int2 = (sort_data[3].int+sort_data[4].int)/2
    tm1 = (7800+sort_data[1].t1+sort_data[1].t2)/2
    tm2 = (sort_data[3].t1+sort_data[3].t2)/2
    app_slope = (int2-int1)/(tm2-tm1)
    dint1 = (-sort_data[1].int+sort_data[2].int)/2
    dint2 = (-sort_data[3].int+sort_data[4].int)/2
    dt1 = dint1/app_slope
    dt2 = dint2/app_slope
    print(sort_data[1].t1, tm1-dt1, tm1+dt1,sort_data[1].t2)
    print(sort_data[3].t1, tm2-dt2, tm2+dt2, sort_data[3].t2)
    t0 = tm1+(log(1)-int1)/app_slope
    t_die = tm1+(log(0.5)-int1)/app_slope
    tmp1 = tm1+(sort_data[0].int-int1)/app_slope
    to_hr = 24/86400
    print(t0, t_die*to_hr-24, app_slope)

    times = [tmp1, tm1-dt1, tm1+dt1, tm2-dt2, tm2+dt2]
    plot_range = range(30000, 100000, 5000)
    plot_ints = [1+exp(5.478e-5*(x-109185)) for x in plot_range]
    plot(times, [1+exp(x.int) for x in sort_data], 'b.')
    plot(plot_range, plot_ints)
    show()


if __name__ == '__main__':
    main(argv)