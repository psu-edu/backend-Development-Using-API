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

def test_update_weather():
    # First, create a sample entry
    sample = {
        "name": "Update City",
        "main": {"temp": 60.0, "humidity": 40},
        "wind": {"speed": 5.5}
    }
    create_resp = client.post("/weather/", json=sample)
    assert create_resp.status_code == 200
    weather_id = create_resp.json()["id"]

    # Modify the data
    updated = {
        "name": "Updated City",
        "main": {"temp": 65.5, "humidity": 45},
        "wind": {"speed": 6.0}
    }
    update_resp = client.put(f"/weather/{weather_id}", json=updated)
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["name"] == "Updated City"
    assert data["main"]["temp"] == 65.5

def test_delete_weather():
    # First, create a resource
    sample = {
        "name": "Delete City",
        "main": {"temp": 75.0, "humidity": 55},
        "wind": {"speed": 8.8}
    }
    create_resp = client.post("/weather/", json=sample)
    assert create_resp.status_code == 200
    weather_id = create_resp.json()["id"]

    # Now delete it
    delete_resp = client.delete(f"/weather/{weather_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Deleted"

    # Check that it's gone
    get_resp = client.get(f"/weather/{weather_id}")
    assert get_resp.status_code == 404

def test_get_weather_by_id():
    # First, create a resource
    sample = {
        "name": "GetByID City",
        "main": {"temp": 68.0, "humidity": 48},
        "wind": {"speed": 4.0}
    }
    create_resp = client.post("/weather/", json=sample)
    assert create_resp.status_code == 200
    weather_id = create_resp.json()["id"]

    # Fetch by ID
    get_resp = client.get(f"/weather/{weather_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["name"] == "GetByID City"
    assert data["main"]["temp"] == 68.0
