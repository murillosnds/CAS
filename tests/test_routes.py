import pytest

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_calculate_hydration(client):
    payload = {
        "weight": 70,
        "age": 30,
        "activity_level": "sedentario",
        "climate": "moderado"
    }
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["water_amount_ml"] == 2450.0
    assert data["water_amount_liters"] == 2.45
    assert "recommendation" in data

def test_invalid_weight(client):
    payload = {
        "weight": -10,
        "age": 30,
        "activity_level": "sedentario",
        "climate": "moderado"
    }
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 422

def test_invalid_age(client):
    payload = {
        "weight": 70,
        "age": 150,
        "activity_level": "sedentario",
        "climate": "moderado"
    }
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 422

def test_get_calculation(client):
    # Primeiro criar um cálculo
    payload = {
        "weight": 70,
        "age": 30,
        "activity_level": "ativo",
        "climate": "quente"
    }
    response = client.post("/api/v1/calculate", json=payload)
    calculation_id = response.json()["id"]
    
    # Buscar o cálculo
    response = client.get(f"/api/v1/calculations/{calculation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calculation_id
    assert data["weight"] == 70

def test_list_calculations(client):
    response = client.get("/api/v1/calculations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)