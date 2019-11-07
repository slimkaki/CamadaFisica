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
import suaBibSignal as bibSignal

from gnu import *

def main():
    print("\n")
    print(" -------------------------------------- ")
    print("|      Sistema SDR feito por          |")
    print("|      Lucas Leal e Rafael Almada      |")
    print("| Camada Física da Computação - Insper |")
    print("|       Engenharia da Computação       |")
    print(" -------------------------------------- ")
    print("\n")

    gnu = gnuRadio()
    print('Digite aqui o texto a ser enviado: ')
    text = str(input('> '))
    gnu.writeTxt(text)



if __name__ == "__main__":
    main()