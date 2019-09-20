
#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
# Lucas Leal Vale e Rafael Almada
####################################################

from enlace import *
import time
from PyCRC.CRC16 import CRC16
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
    self.t0=0
    self.t1=0
    self.tipo=0
    self.find=0
    self.crc = 0
    self.Localcrc=0
  def start(self):

    self.com.rx.clearBuffer()
    self.com.enable()
    print("Initializing Server")



  def WaitInfo(self, noBytes): # noBytes = Number of Bytes

    dataStuff = b'\xf0\xf0\xf0\xf0'
    EoP = b"\xf0\xf1\xf2\xf3"

    while(self.ocioso):

      print("Waiting Communication")

      self.tiempo()
      
      print("Communication attempt identified")

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

          self.MsgBiuld(2)

          self.com.sendData(self.msg)

          self.cont=1

          print("Auth verified")

        else:
          #print("ow")
          time.sleep(1)

      else:
        #print("ola")
        time.sleep(1)

      pass
  

  def receiveImg(self):

    print("Initializing Data Transfer")

    self.cont= int(1)

    tp = int.from_bytes(self.tp,byteorder='little')


    while (self.cont <= tp):

      self.tiempo()
      self.saveP()
      #print(self.np)
      #print(self.tipo)
      if (self.tipo == 3):
        #print(self.find)
        if (self.find>0):
          self.MsgBiuld(4)
          #print(tp)
          #print(self.cont)
          if (self.cont == tp):

            if (self.crc == self.Localcrc): 
              print("LastPack: " + str(self.cont) + "/" + str(tp))
              self.addPayload(boolean = True)
              self.com.sendData(self.msg)
              self.cont+=1

            else:
              self.MsgBiuld(6)
              self.com.sendData(self.msg)

          else:
            print(self.crc)
            print(self.Localcrc)
            if (self.crc == self.Localcrc): 
              self.addPayload()
              self.com.sendData(self.msg)
              self.cont+=1

            else:
              self.MsgBiuld(6)
              self.com.sendData(self.msg)

          toConclude = round((self.cont/tp)*100,1)
          print(f'Enviando pacotes................{toConclude}%\r', end='\r')


        else:

          self.MsgBiuld(6)

          self.com.sendData(self.msg)
          
      else:
        #print("oi")
        time.sleep(1)



  def MsgBiuld(self,tipo):
  #Mensagem do tipo 2: Convida o servidor para iniciar a comunicação

    tipo = tipo.to_bytes(1, byteorder='little')

    payload = 0
    payload = payload.to_bytes(128,byteorder = "little")

    id1 = self.id.to_bytes(1, byteorder='little')
    Localcrc = self.Localcrc.to_bytes(2, byteorder='little')

    #print("Numero atual do pack ENVIADO: "+ str(int.from_bytes(self.np,byteorder='little')))
    head = id1 + tipo + self.np + self.tp + self.TPayload + Localcrc

    msg = head + payload + self.EoP
    #if(self.tipo==3):
      #print(int.from_bytes(self.np,byteorder='little'))
    self.msg = msg


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

        payload = payload[:self.resto]

    else:

      self.MsgBiuld(6)
      self.com.sendData(self.msg)
    
    self.Payload += payload


    
  def savePackage(self,head):
    #salvando informacoes do head

    self.np = head[2:6]
    
    self.tp = head[6:10]

    self.TPayload = head[10:14]
    payload,lenpayload =self.com.getData(132)
    
  def tiempo(self):

      self.t0 = time.time()

      while (self.com.rx.getIsEmpty()):
        
        self.t1 = time.time()
        self.Disconected()

        if ((self.t1-self.t0)>=60):

          self.MsgBiuld(5)

          self.com.sendData(self.msg)

          erro, lenerro = self.com.getData(16)
          Tipo = erro[1]
          msg5 = 5
          self.savePackage(erro)

          if Tipo == msg5:

            print("Communication Error")

            self.finish()
        else:
          pass

  def Disconected(self):

    elapsedTime = self.t1-self.t0
    if(elapsedTime %5 == 0):
      self.com.sendData(self.msg)
      print("Remandando msg5")

  def saveP(self):

      atual, lenatual = self.com.getData(16)
      
      self.tipo = atual[1]
      self.np = atual[2:6]
      #print("Numero atual do pack"+str(int.from_bytes(self.np,byteorder='little')))
      TamPack = atual[10:14]

      TamPack = int.from_bytes(TamPack,byteorder='little')

      self.crc = atual[14:]
      self.crc = int.from_bytes(self.crc,byteorder='little')

      print("crc - client... {0}".format(self.crc))
      self.resto = TamPack % 128

      self.corpo, lencorpo = self.com.getData(132)
      payload = self.corpo[:128]
      self.Localcrc = CRC16().calculate(payload)

      #self.Localcrc = int.from_bytes(Localcrc,byteorder='little')
      print("Local-crc-inicial... {0}".format(self.Localcrc))

      self.find = self.corpo.find(self.EoP)



  def save(self):

    print('Image save as: {0}'.format(self.nomeArquivo))
    open(self.nomeArquivo, "wb").write(self.Payload)


  def finish(self):

      print("End of Communication")
      self.com.rx.clearBuffer()
      self.com.disable()

