# Referências do código: 
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

class PassaBaixa(object):

    def __init__(self, sound, sampleRate):
        self.sound = sound
        self.sampleRate = sampleRate # 44100 Hz

    def filtro(self):
        # The Nyquist rate of the signal.
        nyq_rate = self.sampleRate / 2.0
        # The desired width of the transition from pass to stop,
        # relative to the Nyquist rate.  We'll design the filter
        # with a 5 Hz transition width.
        width = 5.0/nyq_rate
        # The desired attenuation in the stop band, in dB.
        ripple_db = 60.0 #dB
        # Compute the order and Kaiser parameter for the FIR filter.
        N, beta = kaiserord(ripple_db, width)
        # The cutoff frequency of the filter.
        cutoff_hz = 4000.0 #hz
        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        # Use lfilter to filter x with the FIR filter.
        filtered_x = lfilter(taps, 1.0, self.sound)
        return filtered_x

