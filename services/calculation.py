from app.schemas import HydrationRequest

class HydrationCalculator:
    """
    Cálculo baseado em recomendações médicas:
    - Base: 35ml por kg de peso
    - Ajustes por idade, atividade e clima
    """
    
    BASE_ML_PER_KG = 35
    
    ACTIVITY_MULTIPLIER = {
        "sedentario": 1.0,
        "ativo": 1.3
    }
    
    CLIMATE_MULTIPLIER = {
        "frio": 0.9,
        "moderado": 1.0,
        "quente": 1.2
    }
    
    @classmethod
    def calculate(cls, data: HydrationRequest) -> float:
        base_amount = data.weight * cls.BASE_ML_PER_KG
        
        # Ajuste por idade (idosos precisam de mais atenção)
        age_factor = 1.0
        if data.age > 65:
            age_factor = 1.1
        elif data.age < 18:
            age_factor = 1.05
        
        # Aplicar multiplicadores
        activity_factor = cls.ACTIVITY_MULTIPLIER[data.activity_level]
        climate_factor = cls.CLIMATE_MULTIPLIER[data.climate]
        
        total = base_amount * age_factor * activity_factor * climate_factor
        
        return round(total, 2)
    
    @staticmethod
    def get_recommendation(water_ml: float) -> str:
        liters = water_ml / 1000
        glasses = int(water_ml / 250)
        
        return (
            f"Recomenda-se beber aproximadamente {liters:.2f} litros ({water_ml:.0f}ml) "
            f"de água por dia, o que equivale a cerca de {glasses} copos de 250ml."
        )