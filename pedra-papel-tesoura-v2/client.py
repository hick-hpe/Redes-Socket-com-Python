import socket

HOST = "127.0.0.1"
PORT = 9001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = input("Digite pedra, papel ou tesoura: ")
    s.sendall(msg.encode())

    resposta = s.recv(1024)
    print(resposta.decode())

