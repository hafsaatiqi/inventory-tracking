def test_create_store_unauthorized(client):
    response = client.post("/stores/", json={"name": "Test Store"})
    assert response.status_code == 401  # Unauthorized

def test_create_store_authorized(client):
    response = client.post(
        "/stores/",
        json={"name": "Test Store"},
        auth=("admin", "admin123"),
    )
    assert response.status_code == 200