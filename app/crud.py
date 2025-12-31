from sqlalchemy.orm import Session
from app.models import HydrationCalculation
from app.schemas import HydrationRequest

def create_calculation(db: Session, data: HydrationRequest, water_amount: float):
    db_calculation = HydrationCalculation(
        weight=data.weight,
        age=data.age,
        activity_level=data.activity_level,
        climate=data.climate,
        water_amount_ml=water_amount
    )
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation

def get_calculation(db: Session, calculation_id: int):
    return db.query(HydrationCalculation).filter(
        HydrationCalculation.id == calculation_id
    ).first()

def get_calculations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(HydrationCalculation).offset(skip).limit(limit).all()