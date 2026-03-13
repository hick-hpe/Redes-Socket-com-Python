# Servidor
import socket

HOST = "0.0.0.0"
PORT = 9002


def decidir_vencedor(j1, j2):

    if j1 == j2:
        return "empate"
    elif (
        j1 == 'tesoura' and j2 == 'papel' or
        j1 == 'papel' and j2 == 'pedra' or
        j1 == 'pedra' and j2 == 'tesoura'
    ):
        return "v1"
    elif (
        j2 == 'tesoura' and j1 == 'papel' or
        j2 == 'papel' and j1 == 'pedra' or
        j2 == 'pedra' and j1 == 'tesoura'
    ):
        return "v2"
        


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)

    print("Servidor iniciado...")

    dados = []

    conn1, addr1 = s.accept()
    print(f"Cliente 1 conectou!!")

    conn2, addr2 = s.accept()
    print(f"Cliente 2 conectou!!")

    data1 = conn1.recv(1024).decode()
    
    data2 = conn2.recv(1024).decode()

    print("Fim de jogo:")
    print(f"J1: {data1}")
    print(f"J2: {data2}")
    
    r1, r2 = "r1", "r2"
    resposta_jogada = decidir_vencedor(data1, data2)
    print(resposta_jogada)
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
