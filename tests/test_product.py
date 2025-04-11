# tests/test_product.py

from fastapi.testclient import TestClient
from app.main import app  # Import FastAPI app

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={"name": "cappuccino", "price": 900, "quantity": 10})
    assert response.status_code == 200
    assert response.json()["name"] == "cappuccino"
    assert response.json()["quantity"] == 10

def test_get_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "cappuccino"

def test_update_product():
    response = client.put("/products/1", json={"name": "cappuccino", "price":850, "quantity": 20})
    assert response.status_code == 200
    assert response.json()["name"] == "cappuccino"
    assert response.json()["quantity"] == 20
