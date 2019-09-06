
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
    self.resto = 0



  def start(self):

    self.com.rx.clearBuffer()
    self.com.enable()
    print("+++++++++++++++++++++++iniciando server++++++++++++++++++++++")



  def WaitInfo(self, noBytes): # noBytes = Number of Bytes

    dataStuff = b'\xf0\xf0\xf0\xf0'
    EoP = b"\xf0\xf1\xf2\xf3"

    while(self.ocioso):
      print("+++++++++++++++++++++++Esperando comunicação+++++++++++++++++++++++")


      while (self.com.rx.getIsEmpty()):
        pass

      print("+++++++++++++++tentativa de comunicação identificada+++++++++++++++")
      head, head_size = self.com.getData(noBytes)
      
      cliente_id = head[0]

      Tipo = head[1]

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

          print("+++++++++++++++++++Mensagem confirmada para mim++++++++++++++++++++")

        else:

          time.sleep(1)

      else:

        time.sleep(1)

      pass
  

  def receiveImg(self):

    print("++++++++++++++++++++continuando comunicacao++++++++++++++++++++++++")

    self.cont=int(1)

    np = int(0)

    tp = int.from_bytes(self.tp,byteorder='little')

    while (self.cont <= tp):


      while (self.com.rx.getIsEmpty()):
        pass

      atual, lenatual = self.com.getData(16)
      
      tipo = atual[1]

      TamPack = atual[10:]
      TamPack = int.from_bytes(TamPack,byteorder='little')

      self.resto = TamPack % 128

      np = atual[2:6]

      np = int.from_bytes(np,byteorder='little')

      self.corpo, lencorpo = self.com.getData(132)

      find = self.corpo.find(self.EoP)

      if (tipo == 3):

        if (find>0):
          self.msg4()
          if (self.cont == tp):

            print(" LASTPACK: " + str(self.cont) + "/" + str(tp))
            self.addPayload(boolean = True)
            self.com.sendData(self.msg)

          else:

            self.addPayload()
            self.com.sendData(self.msg)

          print(" Download: " + str(self.cont) + "/" + str(tp))

          self.cont+=1

        else:

          self.msg6()

          self.com.sendData(self.msg)
          
      else:
        print("aqui")
        time.sleep(1)



  def msg2(self):
  
  #Mensagem do tipo 2: Convida o servidor para iniciar a comunicação

    tipo = 2
    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")

    id1 = self.id.to_bytes(1, byteorder='little')

    head = id1 + tipo + self.np + self.tp + self.TPayload

    msg2 = head + payload + self.EoP

    self.msg = msg2

    print("+++++++++++++++++++++++++++enviando msg 2++++++++++++++++++++++++++")



  def msg4(self):
  
  #Mensagem do tipo 4: Confirmacao de recebmento

    tipo = 4

    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0

    payload = payload.to_bytes(128,byteorder = "little")
    
    id1 = self.id.to_bytes(1, byteorder='little')

    head = id1 + tipo + self.np + self.tp + self.TPayload

    msg4 = head + payload + self.EoP

    self.msg = msg4

    print("+++++++++++++++++++++++++++enviando msg 4++++++++++++++++++++++++++")




  def msg6(self):
  
  #Mensagem do tipo 6: ERRO INESPERADO

    tipo = 6
    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")

    id1 = self.id.to_bytes(1, byteorder='little')

    head = id1 + tipo + self.np + self.tp + self.TPayload

    msg6 = head + payload + self.EoP

    self.msg = msg6

    print("+++++++++++++++++++++++++++enviando msg 6++++++++++++++++++++++++++")




  def addPayload(self, boolean = False):

    cutPoint = self.corpo.find(self.EoP)

    if (cutPoint > 0):

      payload = self.corpo[:cutPoint]

      sub = payload.find(self.dataStuff)

      contador = 0

      if sub > 0:

        payload = payload.replace(self.dataStuff, self.EoP)
        contador+=1

      if boolean:

        print("ELE CHEGO O ULTIMO PACOTE ESTA SENDO SALVO")
        payload = payload[:self.resto]

    else:
      self.msg6()
      self.com.sendData(self.msg)
    

    self.Payload += payload

    print('PAYLOADLEN '+str(len(self.Payload)))

    print("+++++++++++++++++++++++  a img esta vino  +++++++++++++++++++++++++")




  def savePackage(self,head):
    #salvando informacoes do head

    self.np = head[2:6]
    
    self.tp = head[6:10]

    self.TPayload = head[10:]

    self.com.getData(132)

    print("+++++++++++++++++++++++ pacote inicial salvo ++++++++++++++++++++++")




  def save(self):

    print('imagem salva no nome {0}'.format(self.nomeArquivo))
    open(self.nomeArquivo, "wb").write(self.Payload)



  def finish(self):

      print("++++++++++++++++++++++++++TERMINOU++++++++++++++++++++++++++++")
      self.com.rx.clearBuffer()
      self.com.disable()

