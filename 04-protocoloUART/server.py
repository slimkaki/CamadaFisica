
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
    self.ocioso = True
    self.id = 1
    self.np = 0
    self.tp = 0
    self.TPayload = 0
    self.cont = 0
    self.EoP= b"\xf0\xf1\xf2\xf3"
    self.msg=b""
    self.corpo=b""
    self.Payload=b""
    self.dataStuff=b'\xf0\xf0\xf0\xf0'

  def start(self):
    self.com.rx.clearBuffer()
    self.com.enable()
    print("+++++++++iniciando server+++++++")
  def WaitInfo(self, noBytes): # noBytes = Number of Bytes

    dataStuff = b'\xf0\xf0\xf0\xf0'
    EoP = b"\xf0\xf1\xf2\xf3"

    while(self.ocioso):
      print("++++++Esperando comunicação+++++++++")
      while (self.com.rx.getIsEmpty()):
        pass
      print("+++++++++tentativa de comunicação identificada++++++++")
      head, head_size = self.com.getData(noBytes)
      
      cliente_id = head[0]
      Tipo = head[1]
      #Tipo = int.from_bytes(Tipo,byteorder = "little")
      msg1 = 1

      #recebeu t1
      if Tipo == msg1:

        #e para mim
        if cliente_id == self.id: 

          self.ocioso = False

          self.savePackage(head)

          self.msg2()

          self.com.sendData(self.msg)

          self.cont=1

          print("+++++++++Mensagem confirmada para mim+++++++")
        else:

          time.sleep(1)

      else:

        time.sleep(1)

      pass
  

  def receiveImg(self):
    print("+++++++continuando comunicacao++++++++++")

    self.cont=1
    tp = int.from_bytes(self.tp,byteorder='little')

    print(str(self.cont) + "<cont sssssssssssss tp>" + str(tp))

    while (self.cont <= tp):
      print(self.cont)
      while (self.com.rx.getIsEmpty()):
        pass

      atual = self.com.getData(16)
      
      tipo = atual[1:2]
      tipo = int.from_bytes(tipo, byteorder='little')
      print("++++++++++++++++++++++++++++++++++++"+tipo)
      self.corpo = self.com.getData(132)
      find = self.corpo.find(self.EoP)
      
      if (tipo == 3):


        if (find>0):
          
          self.addPayload()

          self.msg4()

          self.com.sendData(self.msg)

          self.cont+=1

        else:

          self.msg6()
          self.com.sendData(self.msg)

      else:

        time.sleep(1)

        self.Wait()


  def msg2(self):
  
  #Mensagem do tipo 2: Convida o servidor para iniciar a comunicação

    tipo = 2
    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")

    self.id = self.id.to_bytes(1, byteorder='little')

    self.np = self.np.to_bytes(4, byteorder='little')

    self.tp = self.tp.to_bytes(4, byteorder='little')

    self.TPayload = self.TPayload.to_bytes(6, byteorder='little')

    head = self.id + tipo + self.np + self.tp + self.TPayload

    msg2 = head + payload + self.EoP

    self.msg = msg2

    print("***************enviando msg 2222222**********")


  def msg4(self):
  
  #Mensagem do tipo 2: Convida o servidor para iniciar a comunicação

    tipo = 4
    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")
    


    self.id = self.id.to_bytes(1, byteorder='little')

    self.np = self.np.to_bytes(4, byteorder='little')

    self.tp = self.tp.to_bytes(4, byteorder='little')

    self.TPayload = self.TPayload.to_bytes(6, byteorder='little')

    head = self.id + tipo + self.np + self.tp + self.TPayload

    head = self.id + tipo + self.np + self.tp + self.TPayload

    msg4 = head + payload + self.EoP

    self.msg = msg4

  def msg6(self):
  
  #Mensagem do tipo 2: Convida o servidor para iniciar a comunicação

    tipo = 6
    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")

    self.id = self.id.to_bytes(1, byteorder='little')

    self.np = self.np.to_bytes(4, byteorder='little')

    self.tp = self.tp.to_bytes(4, byteorder='little')

    self.TPayload = self.TPayload.to_bytes(6, byteorder='little')

    head = self.id + tipo + self.np + self.tp + self.TPayload
    head = self.id + tipo + self.np + self.tp + self.TPayload

    msg6 = head + payload + self.EoP

    self.msg = msg6

  def addPayload():

    payload = self.corpo[:128]
    
    sub = payload.find(self.dataStuff)

    if sub > 0:

      payload = payload.replace(self.dataStuff, self.EoP)

    self.Payload += payload
    print("+++++++++++++a img esta vino++++++++++++++++")

  def savePackage(self,head):
    #salvando informacoes do head


    self.tp = head[2:6]
  
    self.tp = int.from_bytes(self.tp,byteorder = "little")

    self.np = head[6:10]

    self.np = int.from_bytes(self.np,byteorder = "little")

    self.TPayload = head[10:]

    self.TPayload = int.from_bytes(self.TPayload,byteorder = "little")

    self.com.getData(132)

    print("+++++++++++++++pacote inicial salvo++++++++++")

  def save(self):
    open(self.nomeArquivo, "wb").write(self.Payload)

  def finish(self):
      print("++++++++++TERMINOU++++++")
      self.com.rx.clearBuffer()
      self.com.disable()



#     # Faz a recepção dos dados

#     open(self.nomeArquivo, "wb").write(Payload)

#     print("\n")
#     print("- - - - - - - - - - - - - - - - -")
#     print("Arquivo foi salvo no diretório com o nome de: {}".format(self.nomeArquivo))
#     print("- - - - - - - - - - - - - - - - -")
#     print("- - - - - - - - - - - - - - - - -")
#     print("\n")
#     print("-------------------------")
#     print(" Comunicação encerrada  ")
#     print("-------------------------")
#     self.com.disable()