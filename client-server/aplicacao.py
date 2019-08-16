
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

import subprocess
from enlace import *
import time
from server import *

print("\n")
print("------------------------------------")
print("   Sistema Client/Server feito por  ")
print("     Lucas Leal e Rafael Almada     ")
print("Camada Física da Computação - Insper")
print("      Engenharia da Computação      ")
print("------------------------------------")
print("\n")

getSerial = subprocess.check_output("python -m serial.tools.list_ports", shell=True)
getSerial = getSerial.decode("utf-8")
getSerial = getSerial.split("\n")
print("Qual porta do seu computador você está utilizando?")
for i in range(len(getSerial)):
  print("{} - {}".format(i, getSerial[i]))
  print("\n")
print("Digite o número da porta...\n")
choice = int(input("> "))
if (choice < len(getSerial) and choice > 0):
  serialName = getSerial[choice]
else:
  print("Digite a porta a seguir:")
  serialName = input("> ")

print("abriu com")

print("\n")
print("---------------------------------")
print("Você deseja ser:")
print("1 - Server")
print("2 - Client")
platform = int(input("> "))

if (platform == 1):
  serv = Server(serialName)
  serv.comunicate()
elif (platform == 2):
  cli = Client(serialName)
  cli.comunicate()
else:
  print("[ERRO] Digite um número")

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM11"                  # Windows(variacao de)
#print("abriu com")

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
#     txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    
    
#     txLen    = len(txBuffer)
#     print(txLen)

#     # Transmite dado
#     print("tentado transmitir .... {} bytes".format(txLen))
#     com.sendData(txBuffer)

#     # espera o fim da transmissão
#     #while(com.tx.getIsBussy()):
#     #    pass
    
    
#     # Atualiza dados da transmissão
#     txSize = com.tx.getStatus()
#     print ("Transmitido       {} bytes ".format(txSize))

#     # Faz a recepção dos dados
#     print ("Recebendo dados .... ")
    
#     #repare que o tamanho da mensagem a ser lida é conhecida!     
#     rxBuffer, nRx = com.getData(txLen)

#     # log
#     print ("Lido              {} bytes ".format(nRx))
    
#     print (rxBuffer)

    

#     # Encerra comunicação
#     print("-------------------------")
#     print("Comunicação encerrada")
#     print("-------------------------")
#     com.disable()

#     #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
# if __name__ == "__main__":
#     main()
