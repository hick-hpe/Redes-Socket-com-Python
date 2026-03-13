import socket
import threading

HOST = "0.0.0.0"
PORT = 9001

jogada1 = None
jogada2 = None

def receber_jogada(conn, jogador):
    global jogada1, jogada2

    jogada = conn.recv(1024).decode().strip().lower()

    if jogador == 1:
        jogada1 = jogada
    else:
        jogada2 = jogada


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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))

    s.listen(2)

    print("Servidor iniciado!!!")
    print("Esperando jogadores...")

    conn1, addr1 = s.accept()
    print("Cliente 1 conectou")

    conn2, addr2 = s.accept()
    print("Cliente 2 conectou")

    t1 = threading.Thread(target=receber_jogada, args=(conn1, 1))
    t2 = threading.Thread(target=receber_jogada, args=(conn2, 2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Fim de jogo:")
    print("J1:", jogada1)
    print("J2:", jogada2)

    resultado = decidir_vencedor(jogada1, jogada2)

    if resultado == "v1":
        r1 = "Voce venceu!!!"
        r2 = "Voce perdeu!!!"

    elif resultado == "v2":
        r1 = "Voce perdeu!!!"
        r2 = "Voce venceu!!!"

    else:
        r1 = "Empate!!!"
        r2 = "Empate!!!"

    r1 = f"Adversario: {jogada2}\n{r1}"
    r2 = f"Adversario: {jogada1}\n{r2}"
    conn1.sendall(r1.encode())
    conn2.sendall(r2.encode())

    conn1.close()
    conn2.close()