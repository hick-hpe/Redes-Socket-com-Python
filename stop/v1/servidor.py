import socket
import threading
from random import randint
import json

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 3
jogadores = {}
alfabeto = [chr(i) for i in range(65, 91)]
letra = None

def getLetra():
    return alfabeto[randint(0, 25)]


def conectar_cliente(conn):
    global letra
    jogadores[conn] = {}
    
    if letra is None:
        letra = getLetra() 

    mensagem = "Letra: {letra}"
    conn.sendall(mensagem.encode())


def receber_palavra(conn):
    resposta = conn.recv(1024).decode()
    obj = json.loads(resposta)
    jogadores[conn] = {
        'pontos': 0,
        'resposta': obj
    }
    

def calcular_pontuacao(conn1, conn2):
    j1 = jogadores[conn1]
    j2 = jogadores[conn2]

    for chave in j1['resposta']:
        if j1['resposta'][chave] == j2['resposta'][chave]:
            j1['pontos'] += 1
            j2['pontos'] += 1
        else:
            j1['pontos'] += 3
            j2['pontos'] += 3

    return [j1['pontos'], j2['pontos']]


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        conn1, addr1 = server.accept()
        conn2, addr2 = server.accept()
        
        # conexao
        t1 = threading.Thread(target=conectar_cliente, args=(conn1,))
        t2 = threading.Thread(target=conectar_cliente, args=(conn2,))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()

        # palavras
        t1 = threading.Thread(target=receber_palavra, args=(conn1,))
        t2 = threading.Thread(target=receber_palavra, args=(conn2,))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()

        # calcular resultado
        pontos = calcular_pontuacao(conn1, conn2)
        conn1.sendall(f"Vc fez {pontos[0]} pontos".encode())
        conn2.sendall(f"Vc fez {pontos[1]} pontos".encode())


if __name__ == "__main__":
    iniciar_servidor()