
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
    print("\nlen do rxBuffer...........{}\n".format(len(rxBuffer)))

    dataStuff = b'\xf0\xf0\xf0\xf0'
    EoP = b"\xf0\xf1\xf2\xf3"

    novaImagem = rxBuffer

    i = rxBuffer.find(EoP)
    novaImagem = rxBuffer[:i]
    print("tirei o EoP ja")

    findDataStuff = novaImagem.find(dataStuff)
    while (findDataStuff > 0):
      print("to no while do dataStuff")
      findDataStuff = novaImagem.find(dataStuff)
      novaImagem = novaImagem[findDataStuff].replace(EoP)

    # contadorEoP = b"" # Contador do EoP
    # i = 0 # contador
    # while (i < len(rxBuffer)):
    #   print("AMIGO ESTO AQUI")
    #   if rxBuffer[i]==b"\xf0":
    #     contadorEoP=b"\xf0"
    #     i+=1
    #   elif rxBuffer[i]==b"\xf1" and contadorEoP==b"\xf0":
    #     contadorEoP+=b"\xf1"
    #     i+=1
    #   elif rxBuffer[i]==b"\xf2" and contadorEoP==b"\xf0\xf1":
    #     contadorEoP+=b"\xf2"
    #     i+=1
    #   elif rxBuffer[i]==b"\xf3" and contadorEoP==b"\xf0\xf1\xf2":
    #     contadorEoP+=b"\xf3"
    #     i+=1
    #   else:
    #     contadorEoP=b""
    #     i+=1
    #     pass
    #   if contadorEoP==b"\xf0\xf1\xf2\xf3":
    #     novaImagem = rxBuffer[:i-4]
    #     break

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

    print("PRINT DO PACOTE ENVIADO: {}".format(rxBuffer))
    print("\n")

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()
