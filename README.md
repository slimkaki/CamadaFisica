# CamadaFisica

## Projetos

### 00 - Loop Back

    Enviando a mensagem para si mesmo por meio de um Arduino, utilizando as portas RX e TX.
    
        - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 01 - Client - Server

    Enviando mensagem de um computador para outro via comunicação UART, utilizando dois Arduinos conectados por meios das portas RX, TX e GND.

        - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 02 - Datagrama

    Enviando mensagem de um computador para outro via comunicação UART, utilizando dois Arduinos conectados por meios das portas RX, TX e GND e utilizando um protocolo de empacotamento, que padroniza o EoP (End of Package) e o Data Stuffing e os coloca junto ao Head e o payload do pacote enviado.

    - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 03 - Fragmentação
    
    O intuito deste projeto é fragmentar os pacotes a serem transmitidos de forma que o tamanho de um pacote deve ser um tamanho anteriormente protocolado entre client e server.

    - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py