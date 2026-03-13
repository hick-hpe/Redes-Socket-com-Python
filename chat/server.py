import threading
import socket

HOST = "0.0.0.0"
PORT = 9000
rodando = True

usuarios = {}

def login(conn):
    # recebe nome e salva
    nome = conn.recv(1024).decode().strip()
    if nome != "":
        resposta = f"Bem vindo(a), {nome}!!!"
        print(f">_ {nome.upper()} entrou no servidor!")

        usuarios[conn] = {
            "nome": nome,
            "thread": None
        }

        conn.sendall(resposta.encode())

        return True
    
    return False


def broadcast_msg(msg):
    # enviar msg para todos os usuarios
    for c in list(usuarios.keys()):
        try:
            c.sendall(msg.encode())
        except:
            pass


def sair_do_chat(conn):
    global rodando

    nome = usuarios[conn]["nome"]
    resposta = f"[EXIT] {nome} saiu do chat..."

    print(resposta)
    broadcast_msg(resposta)

    if conn in usuarios:
        del usuarios[conn]
    conn.close()

    if not usuarios:
        rodando = False
        print("Sala vazia, encerrando o servidor...")


def receber(conn):
    while True:
        try:
            data = conn.recv(1024)

            if not data:
                sair_do_chat(conn)
                break

            msg = data.decode().strip()

            if msg == "/exit":
                sair_do_chat(conn)
                break

            nome = usuarios[conn]['nome']
            msg_formatada = f"{nome}: {msg}"
            print(msg_formatada)
            broadcast_msg(msg_formatada)

        except:
            sair_do_chat(conn)
            break


def criar_thread_cliente(conn):
    if usuarios[conn]["thread"] is None:
        thread = threading.Thread(target=receber, args=(conn,), daemon=True)
        usuarios[conn]["thread"] = thread
        thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    s.settimeout(1)

    print('--- Iniciando ChatServer ---')

    while rodando:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue

        login_feito = None
        if conn not in usuarios:
            login_feito = login(conn)

        if login_feito:
            criar_thread_cliente(conn)
        else:
            rodando = False


