def test_create_product(client):
    response = client.post(
        "/products/",
        json={"name": "Test Item", "price": 100},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0