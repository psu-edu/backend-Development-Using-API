# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_weather():
    response = client.get("/weather/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_weather_invalid():
    # Missing required fields
    response = client.post("/weather/", json={})
    assert response.status_code == 422  # Unprocessable Entity

def test_post_weather_valid():
    sample = {
        "name": "Test City",
        "main": {
            "temp": 70.0,
            "humidity": 50
        },
        "wind": {
            "speed": 10.5
        }
    }
    response = client.post("/weather/", json=sample)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test City"
    assert "id" in data
