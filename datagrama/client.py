
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

    txLen    = len(txBuffer)

    """"
      Por conta do pacote enviado possuir agora, além de um head, um EoP (End of Package), precisamos filtrar o nosso payload
      (o conteúdo do pacote) para o caso de se ter bytes com a mesma informação do EoP, levando a uma transferência incompleta.
      Para isso utilizamos de pacotes chamados de "Data Stuffing" que substitui toda info igual ao EoP como uma combinação específica
      de bytes que, na chegada no servidor é traduzido para sua info original.
    """

    dataStuff = b'\xf0\xf0\xf0\xf0' # data stuffing

    EoP = b'\xf0\xf1\xf2\xf3' # End of Package

    print('- - - - - - - - - - - - - - -')
    print('  Protocolo de Empacotamento ')
    print('\nHead...............{}'.format(tamanhoIntimagem))
    print('\nEoP................{}'.format(EoP))
    print('\nData Stuffing......{}'.format(dataStuff))
    print('\n- - - - - - - - - - - - - - -')
    
    txBuffer = txBuffer.replace(EoP,dataStuff)

    txLen    = len(txBuffer)

    imgSize = txLen.to_bytes(10, byteorder = "little")

    bufferCompleto = imgSize + txBuffer + EoP

    #print("Buffer completo................{}".format(bufferCompleto))

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    self.com.sendData(bufferCompleto)

    t0 = time.time()

    print ("Recebendo dados .... ")

    while (self.com.rx.getIsEmpty()):
      pass

    rxBuffer, nRx = self.com.getData(10)

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