"""
As mensagens apresentadas devem conter nome e IP do cliente e o horário em que o servidor recebeu a mensagem;

O acesso à fila de mensagens no servidor deve ser protegido contra acesso concorrente, utilizando semáforos.
"""

import threading
import socket

HOST = "127.0.0.1"
PORT = 9000


