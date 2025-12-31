# 💧 CAS - Calculator Aquae Sumptionis 

> 👨🏻‍💻 **Feito por: Murillo Sergio**

## Calculadora de ingestão de água por dia! Rápida e fácil de usar.

<p>Esse Projeto foi desenvolvido inteiramente por <a href="https://github.com/murillosnds" target="_blank" rel="noopener noreferrer">@murillosnds</a>.

<div style="display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
</div>

## Como funciona

A API foi desenvolvida em FastAPI (um framework de Python para criação de APIs modernas) e tem como objetivo calcular a quantidade recomendada de ingestão de água por dia.

Para funcionar, a API usa informações como: peso, idade, atividade física (sedentário ou ativo) e clima.

![Postman](https://i.imgur.com/6nSVMnw.png)
Exemplo de request e response da API no Postman
<br>

Ao fazer isso, a resposta é salva no banco de dados do PostgreSQL.

![PostgreSQL](https://i.imgur.com/UQFy7w8.png)


## Como rodar o projeto

```bash
git clone https://github.com/murillosnds/CAS.git
cd CAS
cp .env.exemplo .env
docker-compose up --build
```

## Como rodar o projeto sem Docker 🐳🚫

<ol style="list-style-type: disc; list-style: none;">
<li>1 - Configure o PostgreSQL localmente
<li>2- Instale Redis e RabbitMQ
<li>3- Configure o ambiente:
</ol>

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

<ol style="list-style-type: disc;">
<li>4- Configure o arquivo .env
</ol>

```bash
DB_HOST=localhost
REDIS_HOST=localhost
RABBITMQ_HOST=localhost
```

<ol style="list-style-type: disc;">
<li>5- Crie as tabelas
</ol>

```bash
python create_tables.py
```

<ol style="list-style-type: disc;">
<li>6- Execute a API
</ol>

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
