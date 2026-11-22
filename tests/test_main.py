from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["health"] == "/health"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_add():
    response = client.post("/calculate", json={"operation": "add", "a": 12, "b": 8})
    assert response.status_code == 200
    assert response.json()["result"] == 20.0


def test_calculate_subtract():
    response = client.post("/calculate", json={"operation": "subtract", "a": 20, "b": 7})
    assert response.status_code == 200
    assert response.json()["result"] == 13.0


def test_calculate_multiply():
    response = client.post("/calculate", json={"operation": "multiply", "a": 6, "b": 7})
    assert response.status_code == 200
    assert response.json()["result"] == 42.0


def test_calculate_divide():
    response = client.post("/calculate", json={"operation": "divide", "a": 15, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_calculate_divide_by_zero():
    response = client.post("/calculate", json={"operation": "divide", "a": 10, "b": 0})
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["detail"]


def test_calculate_invalid_operation():
    response = client.post("/calculate", json={"operation": "modulo", "a": 10, "b": 2})
    assert response.status_code == 422  # Pydantic validation error for enum
