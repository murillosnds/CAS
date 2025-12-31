from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import IngestaoAgua

app = FastAPI(title="API de Ingestão de Água")

class Informacoes(BaseModel):
    peso: float
    idade: int
    atividade: str
    clima: str

class Resposta(BaseModel):
    quantidade_de_agua: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/calcular", response_model=Resposta)
def calcular_ingestao_de_agua(
    dados: Informacoes,
    db: Session = Depends(get_db)
):
    ingestao = dados.peso * 35

    atividade_fisica = {
        "sedentario": 0,
        "ativo": 15
    }

    ingestao += atividade_fisica.get(dados.atividade.lower(), 0)

    clima_config = {
        "muito_frio": 0,
        "frio": 200,
        "ameno": 400,
        "quente": 700,
        "muito_quente": 1000
    }

    ingestao += clima_config.get(dados.clima.lower(), 0)

    resultado = round(ingestao / 1000, 2)

    registro = IngestaoAgua(
        peso=dados.peso,
        idade=dados.idade,
        atividade=dados.atividade,
        clima=dados.clima,
        quantidade_de_agua=resultado
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return {"quantidade_de_agua": resultado}
