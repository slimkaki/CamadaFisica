#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################
#             Insper              #
#     Engenharia da Computação    #
#   Camada Física da Computação   #
#  -----------------------------  #
#     Código desenvolvido por:    #
#    Lucas Leal e Rafael Almada   #
#  -----------------------------  #
#     Prof. Rodrigo Carareto      #
###################################

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window


class signalMeu(object):
    def __init__(self):
        self.init = 0

    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')
        plt.savefig('fourier.png')
        #plt.show()