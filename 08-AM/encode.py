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
import suaBibSignal as bibSignal
import time, sys
import soundfile as sf
import filtroPassaBaixa as fpb

class Encode(object):

    def __init__(self):
        self.freqAmostra = 44100
        self.freq1 = 0
        self.freq2 = 0
        self.amplitude = 1 # amplitude da onda formada
        self.duration = 120 # segundos
        self.gainX  = 0.3
        self.gainY  = 0.3

    def main(self, sound):
        sound, samplerate = sf.read(sound)
        lista = self.getSoundWaveList(sound)
        b = bibSignal.signalMeu()
        # sd.play(lista, self.freqAmostra)
        # sd.wait()
        b.plotFFT(lista, self.freqAmostra, 'encodeFourier.png')
        pb = self.normalize(lista)
        b.plotFFT(pb, self.freqAmostra, 'encodeFourier+FiltroPassaBaixa.png')

        S = self.moduleAM(pb)
        b.plotFFT(S, self.freqAmostra, 'encodeFourierModulada.png')

        # b = bibSignal.signalMeu()
        #plt.show()

        print("\nO áudio modulado tocará em 5 segundos")
        t0 = time.time()
        t1 = time.time()
        while (t1-t0 < 5):
            print(str(round(5-(t1-t0))) + str(" segundo(s)\r"), end='\r')
            t1 = time.time()
            time.sleep(1)
        print("")
        print("\n========================")
        print("Iniciando a tocar o áudio!")
        print("========================\n")

        sd.play(S, 14000)
        sd.wait()

        print("")
        print("\n====================")
        print("     Fim do áudio!    ")
        print("====================\n")

        print("+++++++++++++++++++++++++++")
        print("Gráficos salvos em:        ")
        print("./modulacao-sinal-audio.png")
        print("./fourier.png              ")
        print("+++++++++++++++++++++++++++")

        b.plotFFT(S, self.freqAmostra, 'fourier-encode.png')
        plt.figure(num=None, figsize=(14, 14), dpi=80, facecolor='w', edgecolor='k')
        plt.subplot(3,1,1)
        self.graficoTempo(lista, 'Sinal de áudio original', 'orange')
        plt.subplot(3,1,2)
        self.graficoTempo(pb, 'Sinal de áudio normalizado', 'purple')
        plt.subplot(3,1,3)
        self.graficoTempo(S, 'Sinal de áudio modulado em AM', 'green')
        plt.savefig('modulacao-sinal-audio.png')

    def graficoTempo(self, signal, title, color):
        duration = len(signal)/self.freqAmostra
        tempo = np.linspace(0, duration, num=len(signal))
        plt.plot(tempo, signal, color)
        plt.title(title)
        plt.xlabel('Tempo (s)')
        

    def getSoundWaveList(self, sound):
        lista=[]
        for i in sound:
            lista.append(i[1])
        return lista


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
        f = fpb.PassaBaixa(module, self.freqAmostra)
        pb = f.filtro()
        return pb

    def moduleAM(self, pb):
        f = 14000 # freq a ser modulada em Hz
        b = bibSignal.signalMeu()
        Cx, Cs = b.generateSin(f, self.amplitude, self.duration, self.freqAmostra)
        # S = Cs*pb
        S = []
        for m in range(len(pb)):
            S.append(Cs[m]*pb[m])
        return S


    def discagem(self):
        """
        Método que salva as frequencias a serem utilizadas na discagem
        """
        bib = bibSignal.signalMeu()
        self.printTeclado()
        print("Qual tecla você deseja discar?")
        num = str(input("> ")).upper()
        array = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['X', '0', '#', 'D']]
        linha = [697, 770, 852, 941]
        coluna = [1209, 1336, 1477, 1633]
        counter = 0
        i=0
        while (i <= len(array)):
            if (num in array[i]):
                self.freq1 = linha[i]
                self.freq2 = coluna[array[i].index(num)]
                print("\n-----------------------")
                print(f"Frequência 1: {self.freq1} Hz")
                print(f"Frequência 2: {self.freq2} Hz")
                print("-----------------------\n")
                break

            elif (counter==3):
                print("Valor inválido")
                print("Digite outro valor:")
                num = str(input("> ")).upper()
                i = 0
                counter = 0
                continue

            i += 1
            counter+=1

        sine_freq1 = bib.generateSin(self.freq1, self.amplitude, self.duration, self.freqAmostra)
        sine_freq2 = bib.generateSin(self.freq2, self.amplitude, self.duration, self.freqAmostra)
        sine = sine_freq1[1] + sine_freq2[1]
        print("\n=====================================")
        print(f"Gerando Tom referente ao símbolo : {num}")
        print("=====================================\n")
        sd.play(sine, self.freqAmostra)
        plt.plot(sine_freq1[0], sine)
        plt.axis([0.165,0.190,-2,2])
        plt.savefig('sinewave.png')
        #plt.show()
        sd.wait()

        sys.exit()
        

    def todB(self, s):
        """
        Converte intensidade em Db
        """
        sdB = 10*np.log10(s)
        return(sdB)
    
    def printTeclado(self):
        """
        Apenas printa o teclado de teclas que podem ser "pressionadas"
        """
        print("Teclas disponíveis a serem pressionadas:\n")
        array = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['X', '0', '#', 'D']]
        print(" ----------------- ")
        for i in array:
            print(f"| |{i[0]}| |{i[1]}| |{i[2]}| |{i[3]}| |")
        print(" ----------------- \n")


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)