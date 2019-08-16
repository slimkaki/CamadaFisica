
#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

from enlace import *
import time

class Server(object):

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
    print ("iniciando recebimento:")
    while(self.com.rx.getIsEmpty()):
      print("  ")
      print("-------------------------------")
      print("Aguardando pacote de informação")
      pass

    rxBuffer, nRx = self.com.getData(4)
    print ("Leitura do tamanho da imagem em hexa..........................{}  ".format(nRx))
    tamanhoIntimagem = int.from_bytes(rxBuffer, byteorder = "little")
    print ("Leitura do tamanho da imagem..................................{}  ".format(tamanhoIntimagem))

    rxBuffer, nRx = self.com.getData(tamanhoIntimagem)

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    # log
    print ("Lido........................{} bytes ".format(nRx))

    open(self.nomeArquivo, "wb").write(rxBuffer)

    print("\n")
    print("- - - - - - - - - - - - - - - - -")
    print("Arquivo foi salvo no diretório com o nome de: {}".format(self.nomeArquivo))
    print("- - - - - - - - - - - - - - - - -")
    print("Tentando enviar confirmação do tamanho recebido ao client")
    print("- - - - - - - - - - - - - - - - -")
    print("\n")

    imgSizeConfirmation = nRx.to_bytes(4, byteorder = "little")

    self.com.sendData(imgSizeConfirmation)

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()