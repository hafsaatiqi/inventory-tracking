def test_rate_limiting(client):
    for _ in range(10):
        response = client.get("/products/")
        assert response.status_code == 200
    # 11th request should be throttled
    assert client.get("/products/").status_code == 429