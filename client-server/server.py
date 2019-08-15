
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


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)
print("abriu com")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

   

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("iniciando recebimento:")
  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
    #exemplo 1
    #ListTxBuffer =list()
    #for x in range(1,10):
    #    ListTxBuffer.append(x)
    #txBuffer = bytes(ListTxBuffer)
    
    #exemplo2
    #txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    
    
    #txLen    = len(txBuffer)
    #print(txLen)

    # Transmite dado
    #print("tentado transmitir .... {} bytes".format(txLen))
    #com.sendData(txBuffer)

    # espera o fim da transmissão
<<<<<<< HEAD
    while(com.tx.getIsBussy()):
      pass
    
    size = com.rx.getNData(3)

    txLen = int.from_bytes(size, byteorder = "big")
=======
    while(com.rx.getIsEmpty()):
       pass
    rxBuffer, nRx = com.getData(4)
    print ("Leitura do tamanho da imagem em hexa.............       {}  ".format( len(rxBuffer)))
    tamanhoIntimagem = int.from_bytes(rxBuffer, byteorder = "little")
    print ("Leitura do tamanho da imagem..............       {}  ".format( tamanhoIntimagem))
    #txLen = int.from_bytes(size, byteorder = "big")
    #print("    ")
    #print(txLen)
    #print("    ")
>>>>>>> 33d9d81722aa399a34f7666845ec20b9b9a0d9f3
    # Atualiza dados da transmissão
    #txSize = com.tx.getStatus()
    #print ("Transmitido       {} bytes ".format(txSize))

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    
    #repare que o tamanho da mensagem a ser lida é conhecida!     
    #rxBuffer, nRx = com.getData(tamanhoIntimagem)

    # log
    print ("Lido              {} bytes ".format(nRx))
    
    print (rxBuffer)

    open("uhul.jpg","wb").write(rxBuffer)

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
