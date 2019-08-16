
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

class Client(object):

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

    print ("gerando dados para transmissao :")

    txBuffer= open(self.nomeArquivo, "rb").read()

    print("TxBuffer sem converter para int...........{}".format(txBuffer))

    txLen    = len(txBuffer)

    imgSize = txLen.to_bytes(4, byteorder = "little")

    bufferCompleto = imgSize + txBuffer

    print("Buffer completo................{}".format(bufferCompleto))
    print("imgSize...............{}".format(imgSize))

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    self.com.sendData(bufferCompleto)

    t0 = time.time()

    print ("Recebendo dados .... ")

    t1 = time.time()

    vel = txLen/(t1-t0)

    print("\n")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Tempo de transferência........................{}".format(t1-t0))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("\n")
    s
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem141101" # Mac    (variacao de)
# serialName = "COM11"                  # Windows(variacao de)
print("abriu com")

# def main():
#     # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
#     com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
#     # Ativa comunicacao
#     com.enable()

   

#     # Log
#     print("-------------------------")
#     print("Comunicação inicializada")
#     print("  porta : {}".format(com.fisica.name))
#     print("-------------------------")

#     # Carrega dados
#     print ("gerando dados para transmissao :")
  
#       #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
#     #exemplo 1
#     #ListTxBuffer =list()
#     #for x in range(1,10):
#     #    ListTxBuffer.append(x)
#     #txBuffer = bytes(ListTxBuffer)
    
#     #exemplo2
#     #txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
#     txBuffer= open("cavalo.jpeg", "rb").read()
#     #   txBuffer0 = aa.read()
#     #   f = bytearray(txBuffer0)

#     print("TxBuffer sem converter para int...........{}".format(txBuffer))
    
    
#     txLen    = len(txBuffer)
#     print(txLen)

#     imgSize = txLen.to_bytes(4, byteorder = "little")

#     bufferCompleto = imgSize + txBuffer

#     print("Buffer completo................{}".format(bufferCompleto))
#     print("imgSize...............{}".format(imgSize))

#     # Transmite dado
#     print("tentado transmitir .... {} bytes".format(txLen))
#     com.sendData(bufferCompleto)

#     t0 = time.time()

#     # espera o fim da transmissão
#     #while(com.tx.getIsBussy()):
#     #    pass
    
    
#     # Atualiza dados da transmissão
#     #txSize = com.tx.getStatus()
#     #print ("Transmitido       {} bytes ".format(txSize))

#     # Faz a recepção dos dados
#     print ("Recebendo dados .... ")
    
#     #repare que o tamanho da mensagem a ser lida é conhecida!     
#     #rxBuffer, nRx = com.getData(txLen)

#     # log
#     # print ("Lido              {} bytes ".format(nRx))
    
#     # print (rxBuffer)

    
#     t1 = time.time()

#     vel = txLen/(t1-t0)

#     print("\n")
#     print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
#     print("Tempo de transferência........................{}".format(t1-t0))
#     print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
#     print("\n")
#     s
#     # Encerra comunicação
#     print("-------------------------")
#     print("Comunicação encerrada")
#     print("-------------------------")
#     com.disable()

#     #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
# if __name__ == "__main__":
#     main()
