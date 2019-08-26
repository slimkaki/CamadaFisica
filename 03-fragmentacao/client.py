
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
import math

class Client(object):

  def __init__(self, serialName, nomeArquivo):
    self.serialName = serialName
    self.nomeArquivo = nomeArquivo
    self.com = enlace(serialName)

  def comunicate(self):
    self.com.rx.clearBuffer()
    self.com.enable()

    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(self.com.fisica.name))
    print("-------------------------")

    txBuffer= open(self.nomeArquivo, "rb").read()

    txLen    = len(txBuffer)

    """"
      Por conta do pacote enviado possuir agora, além de um head, um EoP (End of Package), precisamos filtrar o nosso payload
      (o conteúdo do pacote) para o caso de se ter bytes com a mesma informação do EoP, levando a uma transferência incompleta.
      Para isso utilizamos de pacotes chamados de "Data Stuffing" que substitui toda info igual ao EoP como uma combinação específica
      de bytes que, na chegada no servidor é traduzido para sua info original.
    """

    dataStuff = b'\xf0\xf0\xf0\xf0' # data stuffing

    EoP = b'\xf0\xf1\xf2\xf3' # End of Package

    print('- - - - - - - - - - - - - - -')
    print('  Protocolo de Empacotamento ')
    print('\nTamanho total............{} bytes'.format(txLen))
    print('\nEoP................{}'.format(EoP))
    print('\nData Stuffing......{}'.format(dataStuff))
    print('\nTamanho de cada pacote......128 bytes'.format())
    print('- - - - - - - - - - - - - - -')
    
    txBuffer = txBuffer.replace(EoP,dataStuff)
    bufferCompleto = txBuffer + EoP
    txLen    = len(bufferCompleto)

    """
    Como é necessário para o pacote ter 128 bytes segundo o protocolo, subtrai-se 4 bytes para formar o head
    e logo calcula-se o número de pacotes a serem enviados com o buffer completo (buffer + EoP) dividido por 124 bytes
    """

    NoP = math.ceil(txLen/124) # Number of Packages (função que arredonda qualquer valor que seja float para cima)
    print('\n===============================================')
    print(' Número de Pacotes a serem enviados.........{}'.format(NoP))
    print('===============================================\n')

    NoP_bytes = NoP.to_bytes(2, byteorder='little') # Transformando NoP em bytes para ser adicionado ao head

    # Cada pacote será formulado e enviado no loop abaixo
    # Serão enviados 120 bytes de payload e 4 reservados para o EoP

    # Respostas do servidor em relação ao recebimento do pacote
    ans0=b"\x00" # EoP não encontrado 
    ans1=b"\x01" # EoP encontrado
    ans2=b"\x02" # EoP encontrado na posição errada
    #ans3=b"\x03" # Tamanho do pacote informado está errado

    byte_slice = 0 # contador que corta o pacote por número de bytes
    i = 0
    t0 = time.time()
    while (i <= NoP):
      j = i.to_bytes(2, byteorder='little')
      head = NoP_bytes + j
      if (byte_slice < txLen):
        buffer = head + txBuffer[byte_slice:byte_slice+120] + EoP
        #print("\nTamanho do pacote enviado.........{}".format(len(buffer)))
        self.com.sendData(buffer)
        #print("\nenviando pacote\n")
        #print('Esperando resposta do servidor...')
        while (self.com.rx.getIsEmpty()):
          #print("CADE INFO\n")
          pass
        conf, tam = self.com.getData(len(ans0))
        if (conf == ans0):
          # Mensagem de erro para pacote onde o EoP não foi encontrado pelo server e é dada re-enviado pelo client
          continue
        elif (conf == ans1):
          # Pacote enviado com sucesso
          toConclude = round((i/NoP)*100,1)
          print('Enviando pacotes................{}%\r'.format(toConclude), end='\r')
          i+=1
          byte_slice+=120
        elif (conf == ans2):
          # print('EoP encontrado na posição errada do pacote....{}'.format(i))
          # print('tentando novamente...\n')
          continue
        else:
          # print('Erro inesperado no pacote {}'.format(i))
          # print('tentando novamente...\n')
          continue

    t1 = time.time()
    tempo = t1-t0
    vel = txLen/(tempo)

    print("\n")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Tempo de transferência (Throughput)........................{} s".format(tempo))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("Velocidade da transmissão......................{} bytes/s".format(vel))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("\n")
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    self.com.disable()