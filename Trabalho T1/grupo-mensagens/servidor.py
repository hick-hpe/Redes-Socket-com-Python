"""
O servidor deve suportar múltiplos clientes simultâneamente, utilizando threads;
"""

import threading
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9000
N_CLIENTES = 2
conectados = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    print('\n--- Iniciando ChatServer ---\n')

    # recebe a conexao do cliente
    while conectados < N_CLIENTES:
        conn, addr = s.accept()

        # recebe o dado
        data = conn.recv(1024)

        # obtem nome, IP e horario
        nome = data.decode()
        IP = addr[0]
        data_mensagem = datetime.now()

        # exibe as informacoes
        print(f"[{nome} ({IP}) {data_mensagem.strftime('%I:%M %p')}]")

        conectados += 1


