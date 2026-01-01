# 💧 CAS - Calculator Aquae Sumptionis 

> 👨🏻‍💻 **Made by: Murillo Sergio**

## Daily water intake calculator! Quick and easy to use.

<p>This project was developed entirely by <a href="https://github.com/murillosnds" target="_blank" rel="noopener noreferrer">@murillosnds</a>.

<div style="display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
</div>

## How it works

The API was developed in FastAPI (a Python framework for creating modern APIs) and aims to calculate the recommended daily water intake.

To function, the API uses information such as weight, age, physical activity (sedentary or active), and climate.

![Postman](https://i.imgur.com/6nSVMnw.png)
Example of API request and response in Postman
<br>

## Headers

![EN-US](https://i.imgur.com/7cHfGAI.png)
<br>
![ES](https://i.imgur.com/cMkww24.png)
<br>
![PT-BR](https://i.imgur.com/DxMXsAO.png)

<hr>

### Body > raw

## en-US - Example

```bash
{
  "weight": 74,
  "age": 20,
  "activity": "sedentary",
  "weather": "hot"
}
```

## es - Ejemplo

```bash
{
  "peso": 74,
  "edad": 20,
  "atividade": "sedentario",
  "clima": "caliente"
}
```

## pt-BR - Exemplo

```bash
{
  "peso": 74,
  "idade": 20,
  "atividade": "ativo",
  "clima": "frio"
}
```

## How to run the project

```bash
git clone https://github.com/murillosnds/CAS.git
cd CAS
docker build -t cas-api .
docker run -p 8000:8000 cas-api
# Open http://localhost:8000/docs
```
