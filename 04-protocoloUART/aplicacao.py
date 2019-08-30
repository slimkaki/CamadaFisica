
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
import sys
from server import *
from client import *


def main():
  print("\n")
  print("------------------------------------")
  print("   Sistema Client/Server feito por  ")
  print("     Lucas Leal e Rafael Almada     ")
  print("Camada Física da Computação - Insper")
  print("      Engenharia da Computação      ")
  print("------------------------------------")
  print("\n")

  OS = getOS()
  if (OS == 'Linux'):
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
      serialName = getSerial[choice].strip()
    else:
      print("Digite a porta a seguir:")
      serialName = input("> ")
    
  else:
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
    serverInit(serialName, nomeArquivo)
    print("Iniciando comunicação server - client via conexão UART ......")
    
  elif (platform == 2):
    print("- - - - - - - - - - - - - - - - - - - - - -")
    print("Informe o nome do arquivo a ser enviado, junto")
    print("  à sua extensão (PNG, JPG, JPEG, etc...)  ")
    nomeArquivo = input("> ")
    print("- - - - - - - - - - - - - - - - - - - - - -")
    clientInit(serialName, nomeArquivo)
  else:
    print("[ERRO] Digite um número")

def clientInit(serialName, nomeArquivo):
  cli = Client(serialName, nomeArquivo)
  cli.comunicate()
  cli.msg1()
  cli.constructPack()
  cli.stopCom()

def serverInit(serialName, nomeArquivo):
  serv = Server(serialName, nomeArquivo)
  serv.comunicate()

def getOS():
  OS = {'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'win32': 'Windows',
    'darwin': 'OS X'}
  actualOS = sys.platform
  if actualOS not in OS:
    return 'Unknown OS'
  else:
    return OS[actualOS]

if __name__ == "__main__":
  main()
