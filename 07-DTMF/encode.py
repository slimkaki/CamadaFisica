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

class Encode(object):

    def __init__(self):
        self.freqAmostra = 44100
        self.freq1 = 0
        self.freq2 = 0
        self.amplitude = 1 # amplitude da onda formada
        self.duration = 2 # segundos
        self.gainX  = 0.3
        self.gainY  = 0.3

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