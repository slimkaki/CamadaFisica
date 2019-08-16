
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
from client import *

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
del getSerial[-1]
print("Qual porta do seu computador você está utilizando?")
for i in range(0, len(getSerial)):
  print("{} - {}".format(i, getSerial[i]))
  print("\n")
print("Digite o número da porta...\n")
choice = int(input("> "))
if (choice < len(getSerial) and choice >= 0):
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
  print("- - - - - - - - - - - - - - - - - - - - - -")
  print("Informe o nome do arquivo a ser salvo, junto")
  print("  à sua extensão (PNG, JPG, JPEG, etc...)  ")
  nomeArquivo = input("> ")
  print("- - - - - - - - - - - - - - - - - - - - - -")
  serv = Server(serialName, nomeArquivo)
  print("Iniciando comunicação server - client via conexão UART ......")
  serv.comunicate()
elif (platform == 2):
  print("- - - - - - - - - - - - - - - - - - - - - -")
  print("Informe o nome do arquivo a ser enviado, junto")
  print("  à sua extensão (PNG, JPG, JPEG, etc...)  ")
  nomeArquivo = input("> ")
  print("- - - - - - - - - - - - - - - - - - - - - -")
  cli = Client(serialName, nomeArquivo)
  cli.comunicate()
else:
  print("[ERRO] Digite um número")
