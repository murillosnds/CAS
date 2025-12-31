import pytest
from app.services.calculation import HydrationCalculator
from app.schemas import HydrationRequest

def test_basic_calculation():
    data = HydrationRequest(
        weight=70,
        age=30,
        activity_level="sedentario",
        climate="moderado"
    )
    result = HydrationCalculator.calculate(data)
    assert result == 2450.0  # 70kg * 35ml

def test_active_person_calculation():
    data = HydrationRequest(
        weight=70,
        age=30,
        activity_level="ativo",
        climate="moderado"
    )
    result = HydrationCalculator.calculate(data)
    assert result == 3185.0  # 70kg * 35ml * 1.3

def test_hot_climate_calculation():
    data = HydrationRequest(
        weight=70,
        age=30,
        activity_level="sedentario",
        climate="quente"
    )
    result = HydrationCalculator.calculate(data)
    assert result == 2940.0  # 70kg * 35ml * 1.2

def test_elderly_calculation():
    data = HydrationRequest(
        weight=70,
        age=70,
        activity_level="sedentario",
        climate="moderado"
    )
    result = HydrationCalculator.calculate(data)
    assert result == 2695.0  # 70kg * 35ml * 1.1

def test_combined_factors():
    data = HydrationRequest(
        weight=80,
        age=25,
        activity_level="ativo",
        climate="quente"
    )
    result = HydrationCalculator.calculate(data)
    # 80 * 35 * 1.0 (age) * 1.3 (active) * 1.2 (hot) = 4368
    assert result == 4368.0