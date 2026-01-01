from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="CAS - Multilingual Water Intake API",
    version="4.0.0"
)

# =====================================================
# MODELO DE ENTRADA (ACEITA PT / EN / ES)
# =====================================================

class InputData(BaseModel):
    peso: Optional[float] = None
    weight: Optional[float] = None

    idade: Optional[int] = None
    age: Optional[int] = None

    atividade: Optional[str] = None
    activity: Optional[str] = None

    clima: Optional[str] = None
    weather: Optional[str] = None


# =====================================================
# MAPAS DE NORMALIZAÇÃO
# =====================================================

ACTIVITY_MAP = {
    # PT
    "sedentario": "sedentary",
    "ativo": "active",
    # EN
    "sedentary": "sedentary",
    "active": "active",
    # ES
    "activo": "active"
}

WEATHER_MAP = {
    # PT
    "frio": "cold",
    "quente": "hot",
    "muito quente": "very_hot",
    # EN
    "cold": "cold",
    "hot": "hot",
    "very hot": "very_hot",
    # ES
    "frío": "cold",
    "caliente": "hot",
    "muy caliente": "very_hot"
}


# =====================================================
# CONFIGURAÇÕES DE CÁLCULO
# =====================================================

ACTIVITY_FACTOR = {
    "sedentary": 1.0,
    "active": 1.5
}

WEATHER_FACTOR = {
    "cold": 1.0,
    "hot": 1.1,
    "very_hot": 1.2
}

AGE_FACTOR = {
    "child": 1.2,
    "young": 1.05,
    "adult": 1.0,
    "elderly": 1.15
}


# =====================================================
# RESPONSE POR IDIOMA
# =====================================================

RESPONSE_FIELDS = {
    "pt-br": {
        "weight": "peso",
        "age": "idade",
        "activity": "atividade",
        "weather": "clima",
        "result": "quantidade_de_agua",
        "unit": "litros/dia"
    },
    "en-us": {
        "weight": "weight",
        "age": "age",
        "activity": "activity",
        "weather": "weather",
        "result": "water_intake",
        "unit": "liters/day"
    },
    "es": {
        "weight": "peso",
        "age": "edad",
        "activity": "actividad",
        "weather": "clima",
        "result": "cantidad_de_agua",
        "unit": "litros/día"
    }
}


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def detect_language(accept_language: str) -> str:
    lang = accept_language.lower()
    if lang.startswith("en"):
        return "en-us"
    if lang.startswith("es"):
        return "es"
    return "pt-br"


def normalize_input(data: InputData):
    peso = data.peso or data.weight
    idade = data.idade or data.age
    atividade = data.atividade or data.activity
    clima = data.clima or data.weather

    if not all([peso, idade, atividade, clima]):
        raise HTTPException(400, "Missing required fields")

    try:
        atividade_norm = ACTIVITY_MAP[atividade.lower()]
        clima_norm = WEATHER_MAP[clima.lower()]
    except KeyError:
        raise HTTPException(400, "Invalid activity or weather")

    return peso, idade, atividade_norm, clima_norm


def age_group(age: int) -> str:
    if age <= 12:
        return "child"
    if age <= 25:
        return "young"
    if age <= 59:
        return "adult"
    return "elderly"


# =====================================================
# ENDPOINT
# =====================================================

@app.post("/calc")
async def calcular_agua(
    data: InputData,
    accept_language: str = Header(default="pt-BR")
):
    idioma = detect_language(accept_language)
    fields = RESPONSE_FIELDS[idioma]

    peso, idade, atividade, clima = normalize_input(data)

    ingestao = peso * 35
    ingestao *= AGE_FACTOR[age_group(idade)]
    ingestao *= ACTIVITY_FACTOR[atividade]
    ingestao *= WEATHER_FACTOR[clima]

    return {
        fields["weight"]: peso,
        fields["age"]: idade,
        fields["activity"]: atividade,
        fields["weather"]: clima,
        fields["result"]: round(ingestao / 1000, 2),
        "unit": fields["unit"]
    }
