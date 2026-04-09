# Desafio MBA Engenharia de Software com IA - Full Cycle

## Instruções para executar o código

### Instalar as dependencias

```sh
pip install -r requirements.txt
```

### Subir o banco de dados

```sh
docker compose up -d
```

### Carregar dados do pdf para dentro do PGvector

```sh
python3 ./src/injest.py
```

### Execute o chat

```sh
  python3 ./src/chat.py
```

Faça uma pergunta
