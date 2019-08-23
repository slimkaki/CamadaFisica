
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time
import interfaceFisica as f

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem142101" # Mac
#serialName = "COM11"                  # Windows(variacao de)
print("abriu com")

# def printSlow(lenString, tempo, theString = "-"):
#   for i in range(len(lenString)):
#     if (theString == "-"):
#       print(theString)
#     else:
#       print(theString[i])
#     time.sleep(tempo)

# def app():
#   com = enlace(serialName)
#   com.enable

#   comEnablePrint("Comunicação inicializada")
#   printSlow(comEnablePrint, 0.5)
#   printSlow(comEnablePrint)
#   printSlow(, 0.5, theString="  porta : {}".format(com.fisica.name))
#   printSlow(comEnablePrint, 0.2)



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    #inter = f("inter")

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("gerando dados para transmissao :")


  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
    #exemplo 1
    #ListTxBuffer =list()
    #for x in range(1,10):
    #    ListTxBuffer.append(x)
    #txBuffer = bytes(ListTxBuffer)
    
    #exemplo2
    # txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    # txBuffer = open("gato.jpg", "rb").read()
    with open("fiadaputa.jpg", "rb")  as aa:
      txBuffer0 = aa.read()
    
    txLen    = len(txBuffer0)
    print(txLen)

    imgSize = txLen.to_bytes(4, byteorder = "big")

    bufferCompleto = imgSize + txBuffer0

    #luz = inter.encode(32000)
    #com.sendData(luz)
    com.sendData(bufferCompleto)

    # recebeu = False
    # while (recebeu==False):
    #   recebeu = com.getData(4)

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    # com.sendData(txBuffer0)

    # espera o fim da transmissão
    # while(com.tx.getIsBussy()):
    #    pass
    
    
    # Atualiza dados da transmissão
    # txSize = com.tx.getStatus()
    # print ("Transmitido       {} bytes ".format(txSize))

    # Faz a recepção dos dados
    #print ("Recebendo dados .... ")
    
    #repare que o tamanho da mensagem a ser lida é conhecida! 
    #rxBuffer, nRx = com.getData(txLen)
    #open("chegouDog.jpg", "wb").write(rxBuffer)

    # log
    #print ("Lido              {} bytes ".format(nRx))
    
    #print (rxBuffer)

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
