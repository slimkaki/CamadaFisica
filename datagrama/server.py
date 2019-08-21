
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

    rxBuffer, nRx = self.com.getData(10)

    print ("Leitura do tamanho da imagem em hexa..........................{}  ".format(nRx))
    tamanhoIntimagem = int.from_bytes(rxBuffer, byteorder = "little")
    print ("Leitura do tamanho da imagem..................................{}  ".format(tamanhoIntimagem))

    rxBuffer, nRx = self.com.getData(tamanhoIntimagem)
    print("\nlen do rxBuffer...........{}\n".format(len(rxBuffer)))

    dataStuff = b'\xf0\xf0\xf0\xf0'

    EoP = b"\xf0\xf1\xf2\xf3"

    novaImagem = rxBuffer

    i = rxBuffer.find(EoP)
    novaImagem = rxBuffer[:i]
    print("EoP retirado")

    findDataStuff = novaImagem.find(dataStuff)

    #caso DataStuff tenha sido colocado na img o codigo abaixo resolve isso
    while (findDataStuff > 0):

      print("Voltando DataStuff para a forma original para n distorcer a img")
      findDataStuff = novaImagem.find(dataStuff)
      novaImagem = novaImagem[findDataStuff].replace(EoP)


    novaImagem = novaImagem.replace(dataStuff, EoP)

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

    imgSizeConfirmation = nRx.to_bytes(10, byteorder = "little")

    self.com.sendData(imgSizeConfirmation)

    print("\n")

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()
