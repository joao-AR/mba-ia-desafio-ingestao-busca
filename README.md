# Desafio MBA Engenharia de Software com IA - Full Cycle

## Instruções para executar o código

## Ciar um ambiente virtual

```sh
  python3 -m venv venv 
  source venv/bin/activate
```

### Instalar as dependências

```sh
pip install -r requirements.txt
```

### Subir o banco de dados

```sh
docker compose up -d
```

### Carregar dados do pdf para dentro do PGvector (ingestão)

```sh
python3 ./src/ingest.py
```

### Execute o chat

```sh
  python3 ./src/chat.py
```
ou

Substitua as perguntas em `run.sh` e execute o comando

```sh
  sh run.sh
```
## Exemplo perguntas com respostas

**PERGUNTA:** Qual o faturamento da Empresa SuperTechIABrazil?
<br>

**RESPOSTA:** R$ 10.000.000,00


**PERGUNTA:** Quantos clientes temos em 2024?
<br>

**RESPOSTA:** Não tenho informações necessárias para responder sua pergunta.