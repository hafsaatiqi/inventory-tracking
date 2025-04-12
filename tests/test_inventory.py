def test_stock_movement_flow(client):
    # 1. Create product and store
    product = client.post("/products/", json={"name": "Test Item", "price": 5.0}).json()
    store = client.post("/stores/", json={"name": "Test Store"}, auth=("admin", "admin123")).json()

    # 2. Stock-in 100 units
    stock_in = client.post(
        "/stock-movements/",
        json={
            "product_id": product["id"],
            "store_id": store["id"],
            "type": "stock_in",
            "quantity": 100,
        },
    )
    assert stock_in.status_code == 200

    # 3. Verify inventory updated
    inventory = client.get(f"/inventory/{store['id']}").json()
    assert inventory[0]["quantity"] == 100

    # 4. Test overselling (should fail)
    oversell = client.post(
        "/stock-movements/",
        json={
            "product_id": product["id"],
            "store_id": store["id"],
            "type": "sale",
            "quantity": 200,
        },
    )
    assert oversell.status_code == 400  # Bad Request