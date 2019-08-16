
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

  def __init__(self, serialName):
    self.serialName = serialName
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

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    # log
    print ("Lido........................{} bytes ".format(nRx))

    nomeArquivo = "cavaloChegou.jpeg"
    open(nomeArquivo, "wb").write(rxBuffer)

    print("\n")
    print("- - - - - - - - - - - - - - - - -")
    print("Arquivo foi salvo no diretório com o nome de: {}".format(nomeArquivo))
    print("- - - - - - - - - - - - - - - - -")
    print("Tentando enviar confirmação do tamanho recebido ao client")
    print("- - - - - - - - - - - - - - - - -")
    print("\n")

    imgSizeConfirmation = nRx.to_bytes(4, byteorder = "little")

    self.com.sendData(imgSizeConfirmation)

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()



# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem141101" # Mac    (variacao de)
# #serialName = "COM5"                  # Windows(variacao de)
# print("abriu com")

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
#     print ("iniciando recebimento:")
  
#       #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
#     #exemplo 1
#     #ListTxBuffer =list()
#     #for x in range(1,10):
#     #    ListTxBuffer.append(x)
#     #txBuffer = bytes(ListTxBuffer)
    
#     #exemplo2
#     #txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    
    
#     #txLen    = len(txBuffer)
#     #print(txLen)

#     # Transmite dado
#     #print("tentado transmitir .... {} bytes".format(txLen))
#     #com.sendData(txBuffer)

#     # espera o fim da transmissão

#     while(com.rx.getIsEmpty()):
#       print("  ")
#       print("-------------------------------")
#       print("Aguardando pacote de informação")
#       pass

#     rxBuffer, nRx = com.getData(4)
#     print ("Leitura do tamanho da imagem em hexa..........................{}  ".format(nRx))
#     tamanhoIntimagem = int.from_bytes(rxBuffer, byteorder = "little")
#     print ("Leitura do tamanho da imagem..................................{}  ".format(tamanhoIntimagem))
#     #txLen = int.from_bytes(size, byteorder = "big")
#     #print("    ")
#     #print(txLen)
#     #print("    ")
#     # Atualiza dados da transmissão
#     #txSize = com.tx.getStatus()
#     #print ("Transmitido       {} bytes ".format(txSize))

#     rxBuffer, nRx = com.getData(tamanhoIntimagem)

#     # Faz a recepção dos dados
#     print ("Recebendo dados .... ")
    
#     #repare que o tamanho da mensagem a ser lida é conhecida!     
#     #rxBuffer, nRx = com.getData(tamanhoIntimagem)

#     # log
#     print ("Lido........................{} bytes ".format(nRx))
    
#     print (rxBuffer)

#     nomeArquivo = "cavaloChegou.jpeg"
#     open(nomeArquivo, "wb").write(rxBuffer)

#     print("\n")
#     print("- - - - - - - - - - - - - - - - -")
#     print("Arquivo foi salvo no diretório com o nome de: {}".format(nomeArquivo))
#     print("- - - - - - - - - - - - - - - - -")
#     print("Tentando enviar confirmação do tamanho recebido ao client")
#     print("- - - - - - - - - - - - - - - - -")
#     print("\n")

#     imgSizeConfirmation = nRx.to_bytes(4, byteorder = "little")

#     com.sendData(imgSizeConfirmation)

    

#     # Encerra comunicação
#     print("-------------------------")
#     print("Comunicação encerrada")
#     print("-------------------------")
#     com.disable()

#     #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
# if __name__ == "__main__":
#     main()
