import socket
import threading
from random import randint
import json

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 3
jogadores = []
alfabeto = [chr(i) for i in range(65, 91)]
letra = None

def getLetra():
    return alfabeto[randint(0, 25)]


def conectar_cliente(conn):
    global letra
    if letra is None:
        letra = getLetra() 
    conn.sendall(f"Letra: {letra}".encode())


def receber_palavra(conn):
    resposta = conn.recv(1024).decode()
    obj = json.loads(resposta)
    jogadores.append(obj)
    

def calcular_pontuacao():
    pontos = [0, 0]
    j1 = jogadores[0]
    j2 = jogadores[1]
    
    chaves = ["cep", "nome", "fruta", "animal"]
    for chave in chaves:
        if j1[chave] == j2[chave]:
            pontos[0] += 1
            pontos[1] += 1
        else:
            pontos[0] += 3
            pontos[1] += 3

    return pontos


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        conn1, addr1 = server.accept()
        conn2, addr2 = server.accept()
        
        # conexao
        t1 = threading.Thread(target=conectar_cliente, args=(conn1))
        t2 = threading.Thread(target=conectar_cliente, args=(conn2))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # palavras
        t1 = threading.Thread(target=receber_palavra, args=(conn1))
        t2 = threading.Thread(target=receber_palavra, args=(conn2))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # calcular resultado
        pontos = calcular_pontuacao()
        print("Jogador1:", pontos[0])
        print("Jogador2:", pontos[1])
        
        conn1.sendall(f"Vc fez {pontos[0]} pontos".encode())
        conn2.sendall(f"Vc fez {pontos[1]} pontos".encode())


if __name__ == "__main__":
    iniciar_servidor()