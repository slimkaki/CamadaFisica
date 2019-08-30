
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
import datetime as dt
import math

class Client(object):

  def __init__(self, serialName, nomeArquivo, actualServer):
    self.serialName = serialName
    self.nomeArquivo = nomeArquivo
    self.com = enlace(serialName)
    self.msg = b''
    self.txBuffer = open(self.nomeArquivo, "rb").read()
    self.txLen = len(self.txBuffer)
    self.NoP = b''
    self.actualPackage = 0 # contador de pacotes
    self.byteSlice = 0 # corte do pacote
    self.inicia = False
    self.actualServer = actualServer # id do server atualmente em comunicação

  def start(self):
    """
    Abre a porta para comunicação
    """
    self.com.rx.clearBuffer()
    self.com.enable()

  def startCom(self, idServer):
    """
    Inicia a comunicação com o servidor em questão
    """
    pack0 = self.constructPack(self.actualPackage, self.msg)
    while (self.inicia == False):
      self.sendMsg(pack0)
      time.sleep(5)
      if (self.com.rx.getIsEmpty() == False):
        headAtual, lenHeadAtual = self.com.getData(16)
        if(self.msgType(headAtual) == 2):
          self.inicia = True

  def msgType(self, headAtual):
    """
    Lê mensagem atual e procura o tipo dela (ou tipo 2 ou 4 ou 5 ou 6) e checa se é do servidor certo
    """
    idInformado = headAtual[0]
    if (self.actualServer == idInformado):
      tipoMsg = headAtual[1]
      tipoMsg = int.from_bytes(tipoMsg, byteorder='little')
      if (tipoMsg == 2):
        # Mensagem do tipo 2: Comunicação client-server estabelecida
        self.com.getData(132) # Removendo os 132 bytes do pacote que ainda estão no RxBuffer
        return 2
      elif (tipoMsg == 4):
        # Mensagem do tipo 4: Confirmação do recebimento da mensagem tipo 3 pelo server
        self.com.getData(132)
        return 4
      elif (tipoMsg == 5):
        # Mensagem do tipo 5: Time-out
        self.com.getData(132)
        self.stopCom()
        return 5
      elif (tipoMsg == 6):
        # Mensagem do tipo 6: Mensagem do tipo 3 inválida
        actualPackage = headAtual[2:6]
        self.actualPackage = int.from_bytes(actualPackage, byteorder='little')
        self.com.getData(132)
        return 6
      else:
        # Erro inesperado
        print("ERRO INESPERADO")
        return 0     
    else:
      print("Server encontrado não é o mesmo do informado")
      return 0

  def sendImage(self):
    """
    Inicia a enviar mensagens do tipo 3 com a imagem no payload
    """
    self.stuffData()
    self.actualPackage = 1
    print('\n')
    while (self.actualPackage <= self.NoP):
      self.msg3()
      package = self.constructPack(self.actualPackage, self.msg)
      self.sendMsg(package)
      answerHead, answerLen = self.waitForAnswer(16)
      ansType = self.msgType(answerHead)
      if (ansType == 4):
        toConclude = round((self.actualPackage/self.NoP)*100,1)
        print(f'Enviando pacotes................{toConclude}%\r', end='\r')
        self.increment()
        continue
      elif(ansType == 5):
        break
      elif (ansType == 6):
        continue
      
  def sendMsg(self, msgToBeSent):
    """
    Argumento msgToBeSent é igual ao pacote a ser enviado (message to be sent)
    """
    self.com.sendData(msgToBeSent)

  def increment(self):
    """
    Incrementa 1 ao número do pacote atual e 128 ao corte do payload
    """
    self.actualPackage += 1 # próximo pacote
    self.byteSlice += 128 # 128 bytes

  def waitForAnswer(self, noBytes): # noBytes = Number of Bytes (Integer)
    """
    Aguarda por uma resposta do servidor
    """
    t0 = time.time()
    while (self.com.rx.getIsEmpty()):
      t1 = time.time()
      if ((t1-t0) >= 60):
        self.msg5()
        package = self.constructPack(self.actualPackage, self.msg)
        self.sendMsg(package)
        print("Erro: Time Out. Sem resposta do server.")
        break
      else:
        pass
    pack, lenOfPack = self.com.getData(noBytes)
    return (pack, lenOfPack)

  def constructHead(self, actualPack, tipoMsg):
    """
    Constrói o head de cada pacote. (16 bytes)
    idServer = integer 
    """
    idServer = self.actualServer
    NoP = math.ceil(self.txLen/128) # Number of Packages (Total de pacotes)
    NoP = NoP.to_bytes(4, byteorder='little')
    self.NoP = NoP
    actualPack = actualPack.to_bytes(4, byteorder='little') # Pacote atual
    sizeOfPackage = self.txLen.to_bytes(6, byteorder='little')
    head = idServer + tipoMsg + actualPack + NoP + sizeOfPackage
    return head

  def constructPack(self, actualPack, tipoMsg):
    """
    Constrói cada pacote.
    Head -> 16 bytes
    Payload -> 128 bytes
    EoP -> 4 bytes
    ---------------------
    Total -> 148 bytes
    """
    head = self.constructHead(actualPack, tipoMsg)
    bufferSlice = self.txBuffer[self.byteSlice:self.byteSlice+128]
    EoP = b'\xf0\xf1\xf2\xf3' # End of Package
    package = head + bufferSlice + EoP
    return package

  def stuffData(self):
    """
    Troca o que seria o EoP por um enchimento que, no servidor, será trocado de volta para EoP
    """
    dataStuff = b'\xf0\xf0\xf0\xf0' # data stuffing
    EoP = b'\xf0\xf1\xf2\xf3' # End of Package
    self.txBuffer = self.txBuffer.replace(EoP, dataStuff)
    

  def msg1(self):
    """
    Mensagem do tipo 1: Convida o servidor para iniciar a comunicação
    """
    msg1 = 1
    msg1 = msg1.to_bytes(1, byteorder='little')
    self.msg = msg1

  def msg3(self):
    """
    Mensagem do tipo 3: Envio do payload ciom conteúdo
    """
    msg3 = 3
    msg3 = msg3.to_bytes(1, byteorder='little')
    self.msg = msg3

  def msg5(self):
    """
    Mensagem do tipo 5: Time-Out
    """
    msg5 = 5
    msg5 = msg5.to_bytes(1, byteorder='little')
    self.msg = msg5
    
  def stopCom(self):
    """
    Encerra comunicação
    """
    print("\n-------------------------")
    print("  Comunicação encerrada")
    print("-------------------------")
    self.com.disable()

    # print("-------------------------")
    # print("Comunicação inicializada")
    # print("  porta : {}".format(self.com.fisica.name))
    # print("-------------------------")

    # txBuffer= open(self.nomeArquivo, "rb").read()

    # txLen    = len(txBuffer)

    # """"
    #   Por conta do pacote enviado possuir agora, além de um head, um EoP (End of Package), precisamos filtrar o nosso payload
    #   (o conteúdo do pacote) para o caso de se ter bytes com a mesma informação do EoP, levando a uma transferência incompleta.
    #   Para isso utilizamos de pacotes chamados de "Data Stuffing" que substitui toda info igual ao EoP como uma combinação específica
    #   de bytes que, na chegada no servidor é traduzido para sua info original.
    # """

    # dataStuff = b'\xf0\xf0\xf0\xf0' # data stuffing

    # EoP = b'\xf0\xf1\xf2\xf3' # End of Package

    # print('- - - - - - - - - - - - - - -')
    # print('  Protocolo de Empacotamento ')
    # print('\nTamanho total............{} bytes'.format(txLen))
    # print('\nEoP................{}'.format(EoP))
    # print('\nData Stuffing......{}'.format(dataStuff))
    # print('\nTamanho de cada pacote......128 bytes'.format())
    # print('- - - - - - - - - - - - - - -')
    
    # txBuffer = txBuffer.replace(EoP,dataStuff)
    # bufferCompleto = txBuffer + EoP
    # txLen    = len(bufferCompleto)

    # """
    # Como é necessário para o pacote ter 128 bytes segundo o protocolo, subtrai-se 4 bytes para formar o head
    # e logo calcula-se o número de pacotes a serem enviados com o buffer completo (buffer + EoP) dividido por 124 bytes
    # """

    # NoP = math.ceil(txLen/132) # Number of Packages (função que arredonda qualquer valor que seja float para cima)
    # print('\n===============================================')
    # print(' Número de Pacotes a serem enviados.........{}'.format(NoP))
    # print('===============================================\n')

    # NoP_bytes = NoP.to_bytes(2, byteorder='little') # Transformando NoP em bytes para ser adicionado ao head

    # # Cada pacote será formulado e enviado no loop abaixo
    # # Serão enviados 120 bytes de payload e 4 reservados para o EoP

    # # Respostas do servidor em relação ao recebimento do pacote
    # ans0 = 0 # EoP não encontrado 
    # ans1 = 1 # EoP encontrado
    # ans2 = 2 # EoP encontrado na posição errada
    # #ans3=b"\x03" # Tamanho do pacote informado está errado

    # byte_slice = 0 # contador que corta o pacote por número de bytes
    # i = 0
    # t0 = time.time()
    # while (i <= NoP):
    #   j = i.to_bytes(2, byteorder='little')
    #   head = NoP_bytes + j
    #   if (byte_slice < txLen):
    #     buffer = head + txBuffer[byte_slice:byte_slice+128] + EoP
    #     #print("\nTamanho do pacote enviado.........{}".format(len(buffer)))
    #     self.com.sendData(buffer)
    #     #print("\nenviando pacote\n")
    #     #print('Esperando resposta do servidor...')
    #     while (self.com.rx.getIsEmpty()):
    #       pass
    #     conf, tam = self.com.getData(136)
    #     ans = conf[4]
    #     if (ans == ans0):
    #       # Mensagem de erro para pacote onde o EoP não foi encontrado pelo server e é dada re-enviado pelo client
    #       continue
    #     elif (ans == ans1):
    #       # Pacote enviado com sucesso
    #       toConclude = round((i/NoP)*100,1)
    #       print('Enviando pacotes................{}%\r'.format(toConclude), end='\r')
    #       i+=1
    #       byte_slice+=128
    #       continue
    #     elif (ans == ans2):
    #       # print('EoP encontrado na posição errada do pacote....{}'.format(i))
    #       # print('tentando novamente...\n')
    #       continue
    #     else:
    #       # print('Erro inesperado no pacote {}'.format(i))
    #       # print('tentando novamente...\n')
    #       continue

    # t1 = time.time()
    # tempo = t1-t0
    # vel = txLen/(tempo)
    # minutes = str(dt.timedelta(seconds=tempo))

    # print("\n")
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # print("Tempo de transferência (Throughput)........................{} s".format(tempo))
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # print("Tempo (em minutos)........................{}".format(minutes))
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # print("Velocidade da transmissão......................{} bytes/s".format(vel))
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # print("\n")
    
    # # Encerra comunicação
    # print("-------------------------")
    # print("Comunicação encerrada")
    # print("-------------------------")
