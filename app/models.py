from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentario"
    ACTIVE = "ativo"

class Climate(str, enum.Enum):
    COLD = "frio"
    MODERATE = "moderado"
    HOT = "quente"

class HydrationCalculation(Base):
    __tablename__ = "hydration_calculations"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    activity_level = Column(Enum(ActivityLevel), nullable=False)
    climate = Column(Enum(Climate), nullable=False)
    water_amount_ml = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())