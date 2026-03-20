import socket
import json

HOST = "127.0.0.1"
PORT = 9002


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    # conectar
    cliente.connect((HOST, PORT))
    resposta = cliente.recv(1024).decode("utf-8")
    print(f"[Server] {resposta}")
    
    # enviar palavras
    cep = input("Envie o CEP: ")
    nome = input("Envie o NOME: ")
    fruta = input("Envie o FRUTA: ")
    animal = input("Envie o ANIMAL: ")
    
    obj = {
        "cep": cep,
        "nome": nome,
        "fruta": fruta,
        "animal": animal,
    }
    
    mensagem = json.dumps(obj)
    cliente.sendall(mensagem.encode())
    
    resposta = cliente.recv(1024).decode("utf-8")
    print(f"[Server] {resposta}")