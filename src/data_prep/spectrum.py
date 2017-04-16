import numpy as np
from matplotlib.pyplot import plot, savefig, close, show, xlabel, ylabel

def make_plotter_func(prefix, ar_x1, ar_x2):
    def plotter_func(fn, ar_y1, ar_y2):
        plot(ar_x1, ar_y1)
        plot(ar_x2, ar_y2)
        xlabel('Frequency, kHz')
        ylabel('Power, dB')
        savefig(prefix+fn)
        close()
    return plotter_func

def main():
    'Attenuation model for PSDs retrieved from DoD movies'
    prefix = '../data/psd/'
    names = ['1', '1_bg', '2', '2_bg']
    data = []
    for name in names:
        psd = np.loadtxt(prefix+name+'.txt')
        data.append(psd)

    freqs_1 = np.arange(30.7, 38.4, 0.05)
    freqs_2 = np.arange(30.7, 42.3, 0.05)
    freqs = [freqs_1, freqs_1, freqs_2, freqs_2]
    int_data = [np.interp(freqs[i], data[i][:, 0], data[i][:, 1]) for i in range(4)]

    len1 = freqs_1.shape[0]
    #slope, offset = np.polyfit(int_data[1][:60], int_data[3][:60], 1)
    psd1 = int_data[0]-int_data[1]
    psd2 = int_data[2]-int_data[3]
    #print(slope, offset)
    #plot(freqs_1, psd1)
    #plot(freqs_2, psd2)
    #show()
    att_values = np.array([5.6, 6.2, 6.7, 7.2, 7.75, 8.27, 8.77, 9.25])
    att_sl, att_off = np.polyfit(np.arange(30, 46, 2), att_values, 1)
    sidebands = np.array([33.3, 41.6])
    att_sides = sidebands*att_sl+att_off

    dist_2 = (24.9-8)/(att_sides[1]-att_sides[0])
    gain_2 = psd2+dist_2*(freqs_2*att_sl+att_off)

    att_375 = 37.5*att_sl+att_off
    dist_1 = (10.2-3.7)/(att_375-att_sides[0])
    gain_1 = psd1+dist_1*(freqs_1*att_sl+att_off)
    #sl_12, off_12 = np.polyfit(gain_1, gain_2[:len1], 1)

    plotter_func = make_plotter_func(prefix, freqs_1, freqs_2)
    plotter_func('gain.png', gain_1, gain_2-25)
    plotter_func('orig.png', psd1, psd2)
    print(dist_1, dist_2)

if __name__ == '__main__':
    main()
