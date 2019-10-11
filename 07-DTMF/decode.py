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
import time

class Decode(object):

    def __init__(self):
        self.freqAmostra = 44100
        self.freq1 = 0
        self.freq2 = 0
        self.amplitude = 1 # amplitude da onda formada
        self.duration = 2 # segundos
        self.gainX  = 0.3
        self.gainY  = 0.3

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

        audio = sd.rec(int(self.duration*self.freqAmostra), self.freqAmostra, channels=1)
        sd.wait()
        print("")
        print("\n======================")
        print("Finalizando gravação!")
        print("======================\n")

        t = np.linspace(0, self.duration, self.duration*self.freqAmostra)
        print(f"t = {t}")
        print(f'len(t) = {len(t)}')
        xf, yf = bib.calcFFT(audio, self.freqAmostra)
        # print(f'xf = {xf}')
        # print(f'yf = {yf}')
        bib.plotFFT(audio, self.freqAmostra)
        # plt.figure("F(y)")
        # plt.plot(xf,yf)
        # plt.grid()
        # plt.title('Fourier audio')
    
    def todB(s):
        """
        Converte intensidade em Db
        """
        sdB = 10*np.log10(s)
        return(sdB)





#funcao para transformas intensidade acustica em dB



def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    #sd.default.samplerate = #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    #duration = #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
   
   #faca um print informando que a gravacao foi inicializada
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(inicio,fim,numPontos)

    # plot do gravico  áudio vs tempo!
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    #index = peakutils.indexes(,,)
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()