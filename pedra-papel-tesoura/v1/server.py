# Servidor
import socket

HOST = "0.0.0.0"
PORT = 9000


def decidir_vencedor(j1, j2):
    jogadas = {
        "pedra": "tesoura",
        "tesoura": "papel",
        "papel": "pedra"
    }

    if j1 == j2:
        return "empate"
    elif jogadas[j1] == j2:
        return "v1"
    else:
        return "v2"


def jogada_valida(j):
    return j in ["pedra", "papel", "tesoura"]


def receber_jogada(conn):
    while True:
        jogada = conn.recv(1024).decode().strip().lower()
        if jogada_valida(jogada):
            return jogada
        else:
            conn.sendall("Jogada inválida. Tente novamente.".encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    print("Iniciado partida!!!")
    print("Esperando jogadores...")

    conn1, addr1 = s.accept()
    print(f"Cliente 1 conectou!!")

    conn2, addr2 = s.accept()
    print(f"Cliente 2 conectou!!")

    data1 = receber_jogada(conn1)
    data2 = receber_jogada(conn2)

    if data1 is None or data2 is None:
        print("Um jogador desconectou.")
        conn1.close()
        conn2.close()

    print("Fim de jogo:")
    print(f"J1: {data1}")
    print(f"J2: {data2}")
    
    r1, r2 = "r1", "r2"
    resposta_jogada = decidir_vencedor(data1, data2)
    if resposta_jogada == "v1":
        r1 = "Voce venceu!!!"
        r2 = "Voce perdeu!!!"
    elif resposta_jogada == "v2":
        r1 = "Voce perdeu!!!"
        r2 = "Voce venceu!!!"
    else:
        r1 = "Empate!!!"
        r2 = "Empate!!!"

    conn1.sendall(r1.encode())
    conn2.sendall(r2.encode())

    conn1.close()
    conn2.close()
