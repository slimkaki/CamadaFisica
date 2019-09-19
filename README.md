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

### 04 – Protocolo de comunicação UART ponto a ponto

    O objetivo é implementar um software em dois equipamentos que se comunicam serialmente com padrão UART. 
    A comunicação deve ser feita para envio de um arquivo de um cliente para um servidor. 

    Cada datagrama enviado deve conter no head obrigatoriamente o tipo de mensagem que ele representa e o tamanho do
    payload. Um único byte deve ser reservado no head para conter o número representativo do tipo de mensagem. Dado o tipo de
    mensagem, algumas outras informações devem estar no head, como definido a seguir.

    - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py

### 05 - CRC - Cyclic Redundancy Check

    Objetivo de checar cada pacote e verificar se todos os bits foram enviados corretamente

    - para rodar: python aplicacao.py
          ou no Ubuntu: sudo python3 aplicacao.py