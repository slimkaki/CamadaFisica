
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

    head, head_size = self.com.getData(4)
    print ("\nRecebendo dados .... ")

    Tpack = head[:1]
    Tpack = int.from_bytes(Tpack,byteorder = "little")
    print("Numero total de pacotes.......................{0}".format(Tpack))

    Npack = head[2:]
    Npack = int.from_bytes(Npack,byteorder = "little")

    dataStuff = b'\xf0\xf0\xf0\xf0'

    EoP = b"\xf0\xf1\xf2\xf3"
    Payload = b""
    
    boolean = False

    while (Npack<Tpack):

      if (boolean):
        while(self.com.rx.getIsEmpty()):
          pass
        head, head_size = self.com.getData(4)
        Npack = head[2:]
        Npack = int.from_bytes(Npack,byteorder = "little")
        print("Npack atual ................{0}/{1}".format(Npack,Tpack))
        print("  ")
        print("===========================================")

    
      Pacote, Pack_Size = self.com.getData(124)
      boolean = True

      i = Pacote.find(EoP)
      if (i > 0):
        if (len(Pacote[i:])==len(EoP)):
          Payload += Pacote[:i].replace(dataStuff, EoP)
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

    print('- - - - - - - - - - - - - - - - -')
    print('  Protocolo de Empacotamento ')
    print('Head...............{}'.format(head_size))
    print('EoP................{}'.format(EoP))
    print('Data Stuffing......{}'.format(dataStuff))
    print('- - - - - - - - - - - - - - - - -')
    # Faz a recepção dos dados

    open(self.nomeArquivo, "wb").write(Payload)

    print("\n")
    print("- - - - - - - - - - - - - - - - -")
    print("Arquivo foi salvo no diretório com o nome de: {}".format(self.nomeArquivo))
    print("- - - - - - - - - - - - - - - - -")
    print("Tentando enviar confirmação do tamanho recebido ao client")
    print("- - - - - - - - - - - - - - - - -")
    print("\n")
    print("\n")
    print("-------------------------")
    print(" Comunicação encerrada  ")
    print("-------------------------")
    self.com.disable()
