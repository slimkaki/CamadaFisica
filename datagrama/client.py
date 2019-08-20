
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

    # Para encher nosso Payload com informação inútil que vai evitar o servidor,
    # em uma improbabilidade detectar o padrão do EoP, iremos colocar o Data Stuffing
    # com um padrão único a cada 3 bytes diferentes.

    c = 0 #contador
    dataStuff = ['/xf0/xf0/xf0/xf0']
    txEncoding = txBuffer.split("/")
    i = 0
    while (i < len(txEncoding)):
      if c == 2:
        txEncoding = txEncoding[:i+1] + dataStuff + txEncoding[i+1:]
        i+=2
        c=0
      else:
        i+=1
        c+=1
        pass

    bufferWithStuffedData = "/".join(txEncoding) # txBuffer entrelaçado com data Stuffing, agora novamente em uma string só ao invés de uma lista

    imgSize = txLen.to_bytes(4, byteorder = "little")

    EoP = b'xf0/xf1/xf2/xf3' # End of package

    bufferCompleto = imgSize + bufferWithStuffedData + EoP

    print("Buffer completo................{}".format(bufferCompleto))
    print("imgSize...............{}".format(imgSize))

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    self.com.sendData(bufferCompleto)

    t0 = time.time()

    print ("Recebendo dados .... ")

    t1 = time.time()

    vel = txLen/(t1-t0)

    print("\n")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Tempo de transferência........................{}".format(t1-t0))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("\n")
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()