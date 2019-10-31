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

from encode import *
from decode import *

def main():
    print("\n")
    print(" -------------------------------------- ")
    print("|      Sistema DTMF feito por          |")
    print("|      Lucas Leal e Rafael Almada      |")
    print("| Camada Física da Computação - Insper |")
    print("|       Engenharia da Computação       |")
    print(" -------------------------------------- ")
    print("\n")

    choice = choiceEorR()
    while (choice != "1" or choice != "2"):
        if (choice == "1"):
            emissor()
            break
        elif (choice == "2"):
            receptor()
            break
        else:
            print(f"\nA escolha [{choice}] é inválida\n")
            print("Por favor, tente novamente...\n")
            choice = choiceEorR()
            continue

def emissor():
    # inicializa emissor
    print("\nInicializando o emissor...\n")
    emitter = Encode()
    emitter.main('naruto.wav')
    #emitter.discagem()


def receptor():
    # inicializa receptor
    print("\nInicializando o receptor...\n")
    print('Insira aqui a duração da gravação do áudio:')
    rec = int(input('> '))
    receptor = Decode(rec)
    receptor.main()


def choiceEorR():
    """
    Método que é chamado sempre que é necessário realizar a escolha entre emissor e receptor
    """
    print("Você deseja ser o: ")
    print("1 - Emissor")
    print("2 - Receptor\n")
    choice = input("> ")
    return (choice)


if __name__ == "__main__":
    main()