
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
    self.okPack = {}
    self.errorList = {}

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
    self.msg1()
    pack0 = self.constructPack(self.actualPackage, self.msg)
    stringBusca = 'Buscando servidor'
    stringPonto = ""
    t0 = time.time()
    while (self.inicia == False):
      t1 = time.time()
      if ((t1-t0) >= 20):
        self.msg5()
        timeOutMsg = self.constructPack(self.actualPackage, self.msg)
        self.sendMsg(timeOutMsg)
        break
      self.sendMsg(pack0)
      time.sleep(5)
      print(stringBusca + stringPonto + '\r', end='\r')
      stringPonto += "."
      if (self.com.rx.getIsEmpty() == False):
        headAtual, lenHeadAtual = self.com.getData(16)
        if(self.msgType(headAtual) == 2):
          self.inicia = True

  def msgType(self, headAtual):
    """
    Lê mensagem atual e procura o tipo dela (ou tipo 2 ou 4 ou 5 ou 6) e checa se é do servidor certo
    """
    idInformado = headAtual[0]
    actualServerId = int.from_bytes(self.actualServer, byteorder='little')

    pacoteAtualServer = headAtual[2:6]
    pacoteAtualServer = int.from_bytes(pacoteAtualServer, byteorder='little')

    if (actualServerId == idInformado):
      tipoMsg = headAtual[1]
      #tipoMsg = int.from_bytes(tipoMsg, byteorder='little')
      if (tipoMsg == 2):
        # Mensagem do tipo 2: Comunicação client-server estabelecida
        self.okPack[str(self.actualPackage)] = 2
        self.com.getData(132) # Removendo os 132 bytes do pacote que ainda estão no RxBuffer
        return 2
      elif (tipoMsg == 4):
        # Mensagem do tipo 4: Confirmação do recebimento da mensagem tipo 3 pelo server
        self.okPack[str(self.actualPackage)] = 4
        if (pacoteAtualServer != self.actualPackage):
          self.decrement()
        self.com.getData(132)
        return 4
      elif (tipoMsg == 5):
        # Mensagem do tipo 5: Time-out
        self.errorList[str(self.actualPackage)] = 5
        self.com.getData(132)
        self.stopCom()
        return 5
      elif (tipoMsg == 6):
        # Mensagem do tipo 6: Mensagem do tipo 3 inválida
        self.errorList[str(self.actualPackage)] = 6
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
    NoP = int.from_bytes(self.NoP, byteorder='little')
    print('\n')
    while (self.actualPackage <= NoP):
      self.msg3()
      if (self.actualPackage == NoP):
        package = self.constructPack(self.actualPackage, self.msg, lastPack=True)
      else:
        package = self.constructPack(self.actualPackage, self.msg)
      self.sendMsg(package)
      answerHead, answerLen = self.waitForAnswer(16, package)
      ansType = self.msgType(answerHead)
      if (ansType == 4):
        self.toConcludePrint(NoP)
        self.increment()
        continue
      elif(ansType == 5):
        break
      elif (ansType == 6):
        continue

  def toConcludePrint(self, NoP):
    toConclude = round((self.actualPackage/NoP)*100,1)
    print(f'Enviando pacotes................{toConclude}%\r', end='\r')
      
  def sendMsg(self, msgToBeSent):
    """
    Argumento msgToBeSent é igual ao pacote a ser enviado (message to be sent)
    """
    self.com.sendData(msgToBeSent)

  def decrement(self):
    self.actualPackage -= 1 # próximo pacote
    self.byteSlice -= 128 # 128 bytes

  def increment(self):
    """
    Incrementa 1 ao número do pacote atual e 128 ao corte do payload
    """
    self.actualPackage += 1 # próximo pacote
    self.byteSlice += 128 # 128 bytes

  def waitForAnswer(self, noBytes, package): # noBytes = Number of Bytes (Integer)
    """
    Aguarda por uma resposta do servidor
    """
    t0 = time.time()
    while (self.com.rx.getIsEmpty()):
      time.sleep(1)
      t1 = time.time()
      timedOut = self.checkIfTimeOut(t0, t1)
      disconnect = self.checkDisconnect(t0, t1)
      if(disconnect):
        print(f'Re-enviando pacote {self.actualPackage}')
        self.sendMsg(package)
      if(timedOut):
        self.timeOut()
        break
      else:
        pass
    pack, lenOfPack = self.com.getData(noBytes)
    return (pack, lenOfPack)

  def checkDisconnect(self, t0, t1):
    elapsedTime = t1-t0
    if(elapsedTime%5 == 0):
      return True
    else:
      return False

  def checkIfTimeOut(self, t0, t1):
    elapsedTime = t1-t0
    if(elapsedTime >= 20):
      return True
    else:
      return False

  def timeOut(self):
    self.msg5()
    package = self.constructPack(self.actualPackage, self.msg)
    self.sendMsg(package)


  def constructHead(self, actualPack, tipoMsg):
    """
    Constrói o head de cada pacote. (16 bytes)
    idServer = integer
    ----------------------------
    ID do Servidor -> 1 byte [0]
    Tipo de mensagem -> 1 byte [1]
    Pacote atual -> 4 bytes [2:6]
    Total de pacotes -> 4 bytes [6:10]
    Tamanho total -> 6 bytes [10:16]
    ----------------------------
    """
    idServer = self.actualServer
    NoP = math.ceil(self.txLen/128) # Number of Packages (Total de pacotes)
    NoP = NoP.to_bytes(4, byteorder='little')
    self.NoP = NoP
    actualPack = actualPack.to_bytes(4, byteorder='little') # Pacote atual
    sizeOfPackage = self.txLen.to_bytes(6, byteorder='little')
    head = idServer + tipoMsg + actualPack + NoP + sizeOfPackage
    return head

  def constructPack(self, actualPack, tipoMsg, lastPack = False):
    """
    Constrói cada pacote.
    Head -> 16 bytes
    Payload -> 128 bytes
    EoP -> 4 bytes
    ---------------------
    Total -> 148 bytes
    """
    if(lastPack == False):
      head = self.constructHead(actualPack, tipoMsg)
      bufferSlice = self.txBuffer[self.byteSlice:self.byteSlice+128]
      EoP = b'\xf0\xf1\xf2\xf3' # End of Package
      package = head + bufferSlice + EoP
    else:
      head = self.constructHead(actualPack, tipoMsg)
      bufferSlice = self.txBuffer[self.byteSlice:]
      if (len(bufferSlice) < 128):
        missingInfo = 128-(self.txLen%128)
        bufferSlice += (b'\xf0')*missingInfo
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

  def createLog(self, tempo, vel, minutes):
    NoP = int.from_bytes(self.NoP, byteorder='little')
    idServer = int.from_bytes(self.actualServer, byteorder='little')
    print("- - - - - - - - - - - - - - - - -")
    print("\nCriando Log da transferência")
    print("\n- - - - - - - - - - - - - - - - -")
    ponto = self.nomeArquivo.find(".")
    nome = self.nomeArquivo[:ponto]
    f = open(str("log") + nome + str('.txt'), 'w')
    f.write("LOG DA TRANSFERENCIA DO ARQUIVO: " + self.nomeArquivo)
    f.write("\n-------------------------------------------------")
    f.write("\nComunicando com o servidor: " + str(idServer))
    f.write("\nNúmero de total de pacotes: " + str(NoP))
    f.write("\nTamanho total da imagem: " + str(self.txLen))
    f.write("\nTempo de transferência: " + str(tempo) + " segundos")
    f.write("\nVelocidade de transferência: " + str(vel) + " bytes/segundo")
    f.write("\nTempo em minutos de transferência: " + str(minutes))
    f.write("\n-------------------------------------------------")
    f.write("\nPacotes OK:")
    for o in self.okPack.keys():
      f.write("\nNo pacote " + str(o) + ": Resposta do tipo " + str(self.okPack[o]))
    f.write("\n-------------------------------------------------")
    if (len(self.errorList) > 0):
      f.write("\nErro nos pacotes:")
    for e in self.errorList.keys():
      f.write("\nNo pacote " + str(e) + ": Resposta do tipo " + str(self.errorList[e]))
    f.write("\n---------FIM DO LOG-----------")
    f.close()
    
  def stopCom(self):
    """
    Encerra comunicação
    """
    print("\n----------------------------------------")
    print("         Comunicação encerrada          ")
    print("----------------------------------------")
    self.com.disable()