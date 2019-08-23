
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
    self.com.rx.clearBuffer()
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

    rxBuffer, size = self.com.getData(10)

    overhead = size

    print ("Leitura do tamanho da imagem em hexa..........................{}  ".format(size))
    tamanhoIntimagem = int.from_bytes(rxBuffer, byteorder = "little")
    print ("Leitura do tamanho da imagem..................................{}  ".format(tamanhoIntimagem))

    rxBuffer, nRx = self.com.getData(tamanhoIntimagem)
    # print("\nlen do rxBuffer...........{}\n".format(len(rxBuffer)))

    if (tamanhoIntimagem != nRx):
      print("========================================")
      print("Tamanho informado da imagem está errado!")
      print("========================================")
      ans = b'\x03'
      self.com.sendData(ans)
    else:
      print("=============================================")
      print("Tamanho da imagem foi informada corretamente!")
      print("=============================================")


    overhead += len(rxBuffer)

    dataStuff = b'\xf0\xf0\xf0\xf0'

    EoP = b"\xf0\xf1\xf2\xf3"

    print('- - - - - - - - - - - - - - - - -')
    print('  Protocolo de Empacotamento ')
    print('Head...............{}'.format(tamanhoIntimagem))
    print('EoP................{}'.format(EoP))
    print('Data Stuffing......{}'.format(dataStuff))
    print('- - - - - - - - - - - - - - - - -')

    novaImagem = rxBuffer

    i = rxBuffer.find(EoP)
    if (i > 0):
      if (len(rxBuffer[i:])==len(EoP)):
        novaImagem = rxBuffer[:i]
        print("\nEoP encontrado na posição.......{}".format(i))
        print("\nEoP retirado")
        ans = b'\x01'
        self.com.sendData(ans)
      else:
        print("===========================================")
        print("ERRO: EoP NÃO ENCONTRADO NO LOCAL ESPERADO")
        print("===========================================")
        ans=b'\x02'
        self.com.sendData(ans)
    else:
      print("============================")
      print("ERRO: EoP NÃO ENCONTRADO")
      print("============================")
      ans = b'\x00'
      self.com.sendData(ans)

    overhead = overhead/len(novaImagem)

    novaImagem = novaImagem.replace(dataStuff, EoP)

    print("\nData Stuff substituído pela sequência EoP")

    # Faz a recepção dos dados
    print ("\nRecebendo dados .... ")

    print('\nTamanho do overhead..........{} %'.format(overhead))

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

    # imgSizeConfirmation = len(rxBuffer).to_bytes(10, byteorder = "little")

    # self.com.sendData(imgSizeConfirmation)

    print("\n")

    print("-------------------------")
    print(" Comunicação encerrada  ")
    print("-------------------------")
    self.com.disable()
