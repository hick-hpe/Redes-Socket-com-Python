# Projeto Python - Sockets

Este repositório contém 3 projetos usando sockets TCP em Python, demonstrando comunicação cliente-servidor e uso de threads.

## Pedra-Papel-Tesoura - v1

Versão sequencial do jogo.
O servidor espera um jogador por vez.

### Fluxo
1. Servidor inicia
1. Cliente 1 conecta
1. Cliente 1 envia jogada
1. Cliente 2 conecta
1. Cliente 2 envia jogada
1. Servidor compara vencedor
1. Servidor envia resultado


## Pedra-Papel-Tesoura - v2

Versão simultânea usando threads.
Os dois jogadores podem entrar ao mesmo tempo.

### Fluxo
1. Servidor inicia
1. Cliente 1 e 2 conectam
1. Ambos enviam jogadas
1. Servidor compara jogadas
1. Servidor envia resultado


## Chat

Chat simples usando sockets.

Vários clientes podem se conectar e enviar mensagens em tempo real.

### Fluxo
1. Servidor inicia
1. Cliente conecta
1. Cliente envia nome
1. Servidor registra usuário
1. Cliente envia mensagens
1. Servidor faz broadcast para todos

## Estrutura de pastas
```
redes-sockets-com-python/
│
├─ pedra-papel-tesoura-v1/
│  ├─ server.py
│  └─ client.py
│
├─ pedra-papel-tesoura-v2/
│  ├─ server.py
│  └─ client.py
│
├─ chat/
│  ├─ server.py
│  └─ client.py
│
└─ README.md
```

## Tecnologias utilizadas
- Python
- Sockets TCP
- Threading

## Como executar

- Clone o repositório
    ```bash
    git clone https://github.com/hick-hpe/Redes-Socket-com-Python
    ```

- Entre em algum projeto
    ```bash
    cd projeto
    ```

- Iniciar servidor:
    ```bash
    python server.py
    ```

- Iniciar cliente:
    ```bash
    python server.py
    ```
