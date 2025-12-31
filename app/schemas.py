from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Literal

class HydrationRequest(BaseModel):
    weight: float = Field(..., gt=0, le=300, description="Peso em kg")
    age: int = Field(..., gt=0, le=120, description="Idade em anos")
    activity_level: Literal["sedentario", "ativo"] = Field(..., description="Nível de atividade física")
    climate: Literal["frio", "moderado", "quente"] = Field(..., description="Clima da região")

    @validator('weight')
    def validate_weight(cls, v):
        if v < 30 or v > 300:
            raise ValueError('Peso deve estar entre 30 e 300 kg')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 1 or v > 120:
            raise ValueError('Idade deve estar entre 1 e 120 anos')
        return v

class HydrationResponse(BaseModel):
    id: int
    weight: float
    age: int
    activity_level: str
    climate: str
    water_amount_ml: float
    water_amount_liters: float
    created_at: datetime
    recommendation: str

    class Config:
        from_attributes = True

class HealthCheck(BaseModel):
    status: str
    database: str
    redis: str
    rabbitmq: str