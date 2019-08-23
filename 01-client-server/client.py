
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

from enlace import *
import time

class Client(object):

  def __init__(self, serialName, nomeArquivo):
    self.serialName = serialName
    self.nomeArquivo = nomeArquivo
    self.com = enlace(serialName)

  def comunicate(self):
    self.com.enable()

    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(self.com.fisica.name))
    print("-------------------------")

    print ("gerando dados para transmissao :")

    txBuffer= open(self.nomeArquivo, "rb").read()

    print("TxBuffer sem converter para int...........{}".format(txBuffer))

    txLen    = len(txBuffer)

    imgSize = txLen.to_bytes(4, byteorder = "little")

    bufferCompleto = imgSize + txBuffer

    print("Buffer completo................{}".format(bufferCompleto))
    print("imgSize...............{}".format(imgSize))

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    self.com.sendData(bufferCompleto)

    t0 = time.time()

    print ("Recebendo dados .... ")

    while (self.com.rx.getIsEmpty()):
      pass

    rxBuffer, nRx = self.com.getData(4)

    tamanhoConfirma = int.from_bytes(rxBuffer, byteorder="little")

    print("Confirmação do tamanho da imagem....................{}".format(tamanhoConfirma))
    t1 = time.time()

    tempo = t1-t0

    vel = txLen/(tempo)

    print("\n")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Tempo de transferência........................{}".format(tempo))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Velocidade da transmissão......................{} bytes/s".format(vel))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("\n")
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()