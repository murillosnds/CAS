from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CAS - API para calculo de ingestão de água diária")

class Informacoes(BaseModel):
    peso: float
    idade: int
    atividade: str
    clima: str

class Resposta(BaseModel):
    quantidade_de_agua: float

@app.post("/calcular", response_model=Resposta)
async def calcular_agua(dados: Informacoes):

    ingestao = dados.peso * 35  

    idade_config = {
        "crianca": 1.2,
        "jovem": 1.05,
        "adulto": 1.0,
        "idoso": 1.15
    }

    if dados.idade <= 12:
        faixa = "crianca"
    elif dados.idade <= 25:
        faixa = "jovem"
    elif dados.idade <= 59:
        faixa = "adulto"
    else:
        faixa = "idoso"

    ingestao *= idade_config[dados.idade]

    atividade_config = {
        "sedentario": 1.0,
        "ativo": 1.5
    }

    ingestao *= atividade_config[dados.atividade]

    clima_config = {
        "muito frio": 0.95,
        "frio": 1.0,
        "ameno": 1.0,
        "quente": 1.1,
        "muito quente": 1.2
    }

    ingestao *= clima_config[dados.clima]

    return {"quantidade_de_agua": round(ingestao / 1000, 2)}
