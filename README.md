# CamadaFisica

## Projetos

### 0 - Loop Back

    Enviando a mensagem para si mesmo por meio de um Arduino, utilizando as portas RX e TX.
    
        - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 1 - Client - Server

    Enviando mensagem de um computador para outro via comunicação UART, utilizando dois Arduinos conectados por meios das portas RX, TX e GND.

        - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 2 - Datagrama

    Enviando mensagem de um computador para outro via comunicação UART, utilizando dois Arduinos conectados por meios das portas RX, TX e GND e utilizando um protocolo de empacotamento, que padroniza o EoP (End of Package) e o Data Stuffing e os coloca junto ao Head e o payload do pacote enviado.

    - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py