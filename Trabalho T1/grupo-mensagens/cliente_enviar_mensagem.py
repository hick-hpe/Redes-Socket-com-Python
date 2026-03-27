"""
Antes de enviar mensagens, o cliente deve enviar seu nome ao servidor. Este nome será mostrado nas mensagens;
"""

import threading
import socket

HOST = "127.0.0.1"
PORT = 9000


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    nome = "Henrique"

    s.sendall(nome.encode())
    


