import socket
import threading
from random import randint
import json
import time

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 1
N_RODADAS = 2
N_JOGADORES = 3
jogadores = {}
pontos = {}
alfabeto = [chr(i) for i in range(65, 91)]

def getLetra():
    return alfabeto[randint(0, 25)]


def conectar_cliente(conn):
    global letra, n_rodada_atual
    jogadores[conn] = {
        "nome": f"J{len(jogadores)+1}"
    }
    pontos[conn] = 0


def receber_palavra(conn):
    resposta = conn.recv(1024).decode()
    obj = json.loads(resposta)
    jogadores[conn]["obj"] = obj
    

def calcular_pontuacao():
    chave = list(jogadores.keys())[0]
    temas = list(jogadores[chave]["obj"].keys())
    respostas = {t: {} for t in temas}
    
    i = 1
    for conn in jogadores:
        jog = jogadores[conn]

        for k in jog["obj"]:

            if jog["obj"][k] not in respostas[k]:
                respostas[k][jog["obj"][k]] = [conn]
            else:
                respostas[k][jog["obj"][k]].append(conn)

        i += 1
    

    for k in respostas:
        for res in respostas[k]:
            lista_res = respostas[k][res]
            print(f'[{k}] responderam "{res}": {list(jogadores[c]["nome"] for c in lista_res)}')
    
            if len(lista_res) > 1:
                for conn in lista_res:
                    pontos[conn] += 1
            else:
                pontos[lista_res[0]] += 3


def iniciar_servidor():
    global n_rodada_atual, letra
    n_rodada_atual = 1
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while len(jogadores) < N_JOGADORES:

            conn, addr = server.accept()
        
            # conexao
            thread = threading.Thread(target=conectar_cliente, args=(conn,))
            thread.start()
            thread.join()


        # loop jogo
        while n_rodada_atual <= N_RODADAS:
            
            letra = getLetra()
            
            # enviar mensagem
            for conn in jogadores:
                mensagem = f"Iniciando rodada {n_rodada_atual}/{N_RODADAS}\n"
                mensagem += f"Letra: {letra}\n"
                jog = f"Eu: {jogadores[conn]["nome"]}\n"
                mensagem += jog
                conn.sendall(mensagem.encode())

            # palavras
            for conn in jogadores:
                thread = threading.Thread(target=receber_palavra, args=(conn,))
                thread.start()
                thread.join()
            
            # calcular resultado
            calcular_pontuacao()

            time.sleep(WAITING_TIME)
            for conn in jogadores:
                mensagem = f"Resultado da rodada {n_rodada_atual}:\n"
                mensagem += f"Pontuação: {pontos[conn]} pontos"
                conn.sendall(mensagem.encode())


            if n_rodada_atual == N_RODADAS:
                for conn in jogadores:
                    mensagem_final = "\nResultado final:\n"
                    mensagem += mensagem_final + f"Voce fez {pontos[conn]} pontos"
                    conn.sendall(mensagem.encode())

            n_rodada_atual += 1


if __name__ == "__main__":
    iniciar_servidor()