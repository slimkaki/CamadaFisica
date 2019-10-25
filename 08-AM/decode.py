#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
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
import suaBibSignal as bibSignal
import peakutils, time, math, sys
import filtroPassaBaixa as fpb

class Decode(object):

    def __init__(self, rec):
        self.freqAmostra = 44100
        self.freq1 = 0
        self.freq2 = 0
        self.amplitude = 1 # amplitude da onda formada
        self.duration = 2 # segundos
        self.gainX  = 0.3
        self.gainY  = 0.3
        self.duration = rec
        self.sound = []

    def main(self):
        bib = bibSignal.signalMeu()
        self.recordAudio()
        plt.figure(num=None, figsize=(14, 14), dpi=80, facecolor='w', edgecolor='k')
        self.graficoTempo(self.sound, 'Sinal de áudio capitado', 'orange')

        bib.plotFFT(self.sound, self.freqAmostra, 'fourier-sinal gravado')
        # print(self.sound)
        # print(f'len = {len(self.sound)}')
        self.sound = self.normalize(self.sound)
        self.sound = self.moduleAM(self.sound)

        sd.play(self.sound, self.freqAmostra) 
        sd.wait()
        bib.plotFFT(self.sound, self.freqAmostra, 'Demodulado e filtrado')
        
    def plotDemoduleGraph(self):
        bib = bibSignal.signalMeu()
        xf, yf = bib.calcFFT(self.sound, self.freqAmostra)
        plt.title('Fourier - Demodule')
        plt.plot(xf, yf)
        plt.savefig('Sinal de áudio capitado.png')



    def recordAudio(self):
        print("\nA captura de áudio iniciará em 5 segundos")
        t0 = time.time()
        t1 = time.time()
        while (t1-t0 < 5):
            print(str(round(5-(t1-t0))) + str(" segundo(s)\r"), end='\r')
            t1 = time.time()
            time.sleep(1)
        print("")
        print("\n====================")
        print("Começando a gravar!")
        print("====================\n")
        
        myrecording = sd.rec(self.duration * self.freqAmostra, samplerate=self.freqAmostra, 
        channels=2, blocking=True)# Possivelmente é necessário utilizar "channels=2" no ubuntu
        sd.wait()

        sound = []
        for sublist in myrecording:
            for item in sublist:
                sound.append(item)
        print("")
        print("\n======================")
        print("Finalizando gravação!")
        print("======================\n")
        self.sound = sound




    def getSignal(self):
        """
        Método que pega o sinal enviado por áudio pelo emissor e trata-o para adquirir a tecla que foi
        enviada
        """
        bib = bibSignal.signalMeu()
        sd.default.samplerate = self.freqAmostra
        sd.default.channels = 2
        print("\nA captura de áudio iniciará em 5 segundos")
        t0 = time.time()
        t1 = time.time()
        while (t1-t0 < 5):
            print(str(round(5-(t1-t0))) + str(" segundo(s)\r"), end='\r')
            t1 = time.time()
            time.sleep(1)
        print("")
        print("\n====================")
        print("Começando a gravar!")
        print("====================\n")

        audio1 = sd.rec(int(self.duration*self.freqAmostra), self.freqAmostra, channels=1)
        

        sd.wait()
        audio = []
        for sublist in audio1:
            for item in sublist:
                audio.append(item)
        print("")
        print("\n======================")
        print("Finalizando gravação!")
        print("======================\n")
        #print(audio)
        t = np.linspace(0, self.duration, self.duration*self.freqAmostra)
        #print(f"t = {t}")
        #print(f'len(t) = {len(t)}')
        xf, yf = bib.calcFFT(audio, self.freqAmostra)
        # print(f'xf = {xf}')
        # print(f'yf = {yf}')
        indexes = peakutils.indexes(yf, thres = 0.2, min_dist =100)
        linha = [697, 770, 852, 941]
        coluna = [1209, 1336, 1477, 1633]
        array = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['X', '0', '#', 'D']]

        pico1 = 0
        pico2 = 0
        for i in linha:
            if (math.isclose(i, xf[indexes[0]], abs_tol = 10)):
                pico1 = i 
        for j in coluna:
            if (math.isclose(j, xf[indexes[1]], abs_tol = 10)):
                pico2 = j

        l1 = linha.index(pico1)
        c1 = coluna.index(pico2)
        tecla = array[l1][c1]
        print('\n---------------')
        print(f'Pico 1 = {pico1} Hz\nPico 2 = {pico2} Hz')
        print('---------------\n')
        print('\n==========================')
        print(f"Foi teclado a entrada: [{tecla}]")
        print('==========================\n')

        bib.plotFFT(audio, self.freqAmostra)

        sys.exit()
    
    def todB(s):
        """
        Converte intensidade em Db
        """
        sdB = 10*np.log10(s)
        return(sdB)


    def graficoTempo(self, signal, title, color):
        duration = len(signal)/self.freqAmostra
        tempo = np.linspace(0, duration, num=len(signal))
        plt.plot(tempo, signal, color)
        plt.title(title)
        plt.xlabel('Tempo (s)')
        plt.show()

    def normalize(self, lista):
        """
        Método que normaliza a lista de amplitudes
        """
        
        maximo = max(lista)
        minimo = min(lista)
        module = []
        for e in lista:
            if (maximo > abs(minimo)):
                module.append(e/maximo)
            else:
                module.append(e/abs(minimo))
        # f = fpb.PassaBaixa(module, self.freqAmostra)
        # pb = f.filtro()
        return module

    def moduleAM(self, pb):
        f = 14000 # freq a ser modulada em Hz
        b = bibSignal.signalMeu()
        Cx, Cs = b.generateSin(f, self.amplitude, self.duration, self.freqAmostra)
        # S = Cs*pb
        S = []
        for m in range(len(Cs)):
            S.append(Cs[m]*pb[m])
        f = fpb.PassaBaixa(S, self.freqAmostra)
        pb = f.filtro()
        return pb