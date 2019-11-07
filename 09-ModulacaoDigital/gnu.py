import socket

class gnuRadio(object):
    def __init__(self):
        self.host = "127.0.0.1" # IP do host
        self.port = 1234 # número da porta do socket

    def sendText(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect((self.host, self.port))  # conecta no servidor

        print('Digite aqui o texto a ser enviado: ')
        message = input(" -> ")  # pega o primeiro texto

        while message.lower().strip() != 'bye': # se o texto em algum momento for igual a "bye", a comunicação é terminada
            client_socket.send(message.encode())  # envia a mensagem
            print('Digite outro texto a ser enviado: ')
            message = input("> ")  # pega outro texto
        client_socket.close()  # acaba com a conexão