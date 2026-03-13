import threading
import socket

HOST = "127.0.0.1"
PORT = 9000
rodando = True

def enviar(s):
    global rodando

    while rodando:
        try:
            msg = input()

            if msg.lower() == "/exit":
                s.sendall(b"/exit")
                rodando = False
                break

            s.sendall(msg.encode())

        except:
            break


def receber(s):
    global rodando
    while rodando:
        try:
            resposta = s.recv(1024)
            if not resposta:
                print("Servidor desconectou")
                rodando = False
                break

            resposta = resposta.decode().strip()

            if resposta == "goexit":
                rodando = False
                break
            else:
                print(resposta)
        except:
            break

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        nome = input("Digite seu nome: ")
        s.sendall(nome.encode())

        resposta = s.recv(1024).decode().strip()
        print(resposta)

        t1 = threading.Thread(target=enviar, args=(s,), daemon=True)
        t2 = threading.Thread(target=receber, args=(s,), daemon=True)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

except ConnectionRefusedError:
    print("Servidor não está rodando.")

except KeyboardInterrupt:
    print("\nEncerrando cliente (Ctrl+C)...")

print("Cliente encerrado.")
