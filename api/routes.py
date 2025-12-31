from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pika
import json
import redis

from app.database import get_db
from app.schemas import HydrationRequest, HydrationResponse, HealthCheck
from app.services.calculation import HydrationCalculator
from app.services.cache import cache_service
from app import crud
from app.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/calculate", response_model=HydrationResponse, status_code=201)
async def calculate_hydration(data: HydrationRequest, db: Session = Depends(get_db)):
    """Calcula a quantidade ideal de água diária"""
    
    # Verificar cache
    cache_key = cache_service.generate_key(data.weight, data.age, data.activity_level, data.climate)
    cached = cache_service.get(cache_key)
    
    if cached:
        return HydrationResponse(**cached)
    
    # Calcular quantidade de água
    water_amount = HydrationCalculator.calculate(data)
    
    # Salvar no banco
    db_calculation = crud.create_calculation(db, data, water_amount)
    
    # Enviar para fila RabbitMQ (processamento assíncrono)
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
        channel = connection.channel()
        channel.queue_declare(queue='hydration_calculations', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='hydration_calculations',
            body=json.dumps({"id": db_calculation.id, "water_amount": water_amount})
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao enviar para RabbitMQ: {e}")
    
    # Preparar resposta
    response_data = {
        "id": db_calculation.id,
        "weight": db_calculation.weight,
        "age": db_calculation.age,
        "activity_level": db_calculation.activity_level.value,
        "climate": db_calculation.climate.value,
        "water_amount_ml": water_amount,
        "water_amount_liters": round(water_amount / 1000, 2),
        "created_at": db_calculation.created_at,
        "recommendation": HydrationCalculator.get_recommendation(water_amount)
    }
    
    # Salvar no cache
    cache_service.set(cache_key, response_data)
    
    return HydrationResponse(**response_data)

@router.get("/calculations/{calculation_id}", response_model=HydrationResponse)
async def get_calculation(calculation_id: int, db: Session = Depends(get_db)):
    """Busca um cálculo específico por ID"""
    calculation = crud.get_calculation(db, calculation_id)
    if not calculation:
        raise HTTPException(status_code=404, detail="Cálculo não encontrado")
    
    return HydrationResponse(
        id=calculation.id,
        weight=calculation.weight,
        age=calculation.age,
        activity_level=calculation.activity_level.value,
        climate=calculation.climate.value,
        water_amount_ml=calculation.water_amount_ml,
        water_amount_liters=round(calculation.water_amount_ml / 1000, 2),
        created_at=calculation.created_at,
        recommendation=HydrationCalculator.get_recommendation(calculation.water_amount_ml)
    )

@router.get("/calculations")
async def list_calculations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os cálculos realizados"""
    calculations = crud.get_calculations(db, skip, limit)
    return [
        {
            "id": c.id,
            "weight": c.weight,
            "age": c.age,
            "water_amount_ml": c.water_amount_ml,
            "created_at": c.created_at
        }
        for c in calculations
    ]

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Verifica a saúde dos serviços"""
    status = {"status": "healthy", "database": "ok", "redis": "ok", "rabbitmq": "ok"}
    
    # Verificar Redis
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
    except Exception:
        status["redis"] = "error"
        status["status"] = "degraded"
    
    # Verificar RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
        connection.close()
    except Exception:
        status["rabbitmq"] = "error"
        status["status"] = "degraded"
    
    return status