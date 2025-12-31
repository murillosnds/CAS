from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import hashlib
import json

from database import SessionLocal
from models import IngestaoAgua
from cache import cache
from message_queue import rabbitmq_producer, CalculoMessage

app = FastAPI(title="API de Ingestão de Água")

class Informacoes(BaseModel):
    peso: float
    idade: int
    atividade: str
    clima: str
    user_id: Optional[str] = None  # Adicionado para cache personalizado

class Resposta(BaseModel):
    quantidade_de_agua: float
    from_cache: bool = False  # Indica se veio do cache

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerar_chave_cache(dados: Informacoes) -> str:
    """Gera uma chave única para cache baseada nos dados"""
    dados_str = f"{dados.peso}_{dados.idade}_{dados.atividade}_{dados.clima}"
    if dados.user_id:
        dados_str += f"_{dados.user_id}"
    return f"agua_calc:{hashlib.md5(dados_str.encode()).hexdigest()}"

@app.on_event("startup")
async def startup_event():
    """Inicializa conexões na startup"""
    cache.connect()
    rabbitmq_producer.connect()
    print("Serviços de cache e mensageria inicializados")

@app.on_event("shutdown")
async def shutdown_event():
    """Fecha conexões no shutdown"""
    rabbitmq_producer.close()
    print("Conexões encerradas")

@app.post("/calcular", response_model=Resposta)
def calcular_ingestao_de_agua(
    dados: Informacoes,
    db: Session = Depends(get_db)
):
    # Verifica cache primeiro
    cache_key = gerar_chave_cache(dados)
    cached_result = cache.get(cache_key)
    
    if cached_result:
        return {
            "quantidade_de_agua": cached_result["quantidade_de_agua"],
            "from_cache": True
        }
    
    # Cálculo original
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

    # Armazena no cache
    cache.set(cache_key, {
        "quantidade_de_agua": resultado,
        "peso": dados.peso,
        "idade": dados.idade,
        "atividade": dados.atividade,
        "clima": dados.clima
    }, ttl=300)  # Cache por 5 minutos

    # Registra no banco de dados
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

    # Publica mensagem no RabbitMQ
    mensagem = CalculoMessage(
        peso=dados.peso,
        idade=dados.idade,
        atividade=dados.atividade,
        clima=dados.clima,
        quantidade_de_agua=resultado,
        user_id=dados.user_id
    )
    
    rabbitmq_producer.publish(mensagem.dict())

    return {
        "quantidade_de_agua": resultado,
        "from_cache": False
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    status = {
        "api": "healthy",
        "database": "unknown",
        "redis": "healthy" if cache.is_connected() else "unhealthy",
        "rabbitmq": "unknown"
    }
    
    # Verifica RabbitMQ
    try:
        if rabbitmq_producer.connect():
            status["rabbitmq"] = "healthy"
            rabbitmq_producer.close()
        else:
            status["rabbitmq"] = "unhealthy"
    except:
        status["rabbitmq"] = "unhealthy"
    
    # Verifica database
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        status["database"] = "healthy"
    except:
        status["database"] = "unhealthy"
    
    return status

@app.delete("/cache/clear/{pattern}")
async def clear_cache(pattern: str = "*"):
    """Limpa cache baseado em padrão"""
    cleared = cache.clear_pattern(pattern)
    return {"cleared_keys": cleared, "pattern": pattern}