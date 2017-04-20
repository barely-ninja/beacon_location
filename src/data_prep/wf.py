from sys import argv
from json import load
from moviepy.audio.io.AudioFileClip import AudioFileClip
from scipy.signal import spectrogram
from matplotlib.pyplot import pcolormesh, show, plot, imshow, savefig
from obspy.core.trace import Trace
from obspy.signal.filter import envelope
import numpy as np

def make_spectrogram(snd_arr):
    'spectrogram of whole record'
    f, t, sxx = spectrogram(1e7*snd_arr[:,0], fs=44100, nperseg=512, detrend=False)
    pcolormesh(t, f, np.log10(sxx+1), vmin=0, vmax=10)
    show()

def main(args):
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)
    for clip in cfg:
        s_rate = clip['sampling_rate']
        snd = AudioFileClip(clip['filename'], fps=s_rate)
        clipped = snd.subclip(*clip['time_range'])
        snd_arr = clipped.to_soundarray(fps=s_rate)
        if clip['window'][1]==-1:
            make_spectrogram(snd_arr)
        tr = Trace(data=snd_arr[:, 0], header={'sampling_rate':s_rate})
        filt_tr = tr.filter('bandpass', freqmin=clip['filter'][0]*1000, freqmax=clip['filter'][1]*1000)
        wl = clip['fold']
        envs = []
        for ping in filt_tr.slide(window_length=wl, step=wl, include_partial_windows=True):
            ping_slice = np.array(ping.data)
            ping_slice.resize(int(wl*s_rate))
            wind_ping = ping_slice[clip['window'][0]:clip['window'][1]]
            env = np.array(envelope(wind_ping))
            envs.append(np.log10(env+1))
        data = np.array(envs)
        imshow(data.T, aspect='auto')#, clim=(2e-4, 1e-3))
        #show()
        savefig(clip['clip_name']+'.png')


if __name__ == '__main__':
    main(argv)

