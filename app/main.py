from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app import models
from app import crud
from app import schemas
from datetime import datetime

app = FastAPI()

# Initialize database
init_db()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
 
@app.get("/")
def read_root():
    container_id = os.getenv("HOSTNAME")
    return {"message": f"Inventory Tracking API container {container_id}"}

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Security
import secrets
from fastapi import Request

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin123")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
  

@app.post("/products/")  
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)  
    db_product = crud.create_product(db, product)

    crud.create_audit_log(
        db=db,
        username=credentials.username,
        action="CREATE_PRODUCT",
        target_table="products",
        target_id=db_product.id,
        details=f"Created product '{product.name}'",
    )

    return db_product

from typing import List

# @app.get("/products/", response_model=List[schemas.Product])
# def get_products(db: Session = Depends(get_db)):
#     return crud.get_products(db)

# app/main.py
@app.post("/stock-movements/")
async def create_stock_movement(
    movement: schemas.StockMovementCreate,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security)
):
    authenticate(credentials)  

    db_movement = crud.create_stock_movement(db=db, movement=movement)

    crud.create_audit_log(
        db=db,
        username=credentials.username,
        action="CREATE_STOCK_MOVEMENT",
        target_table="stock_movements",
        target_id=db_movement.id,
        details=f"Created stock movement: {movement.type} of product ID {movement.product_id}, quantity {movement.quantity}"
    )

    return db_movement

from datetime import datetime

@app.get("/stock-movements/")
@limiter.limit("10/minute")
def get_stock_movements(
    request: Request,
    db: Session = Depends(get_db),
    store_id: int = None,
    product_id: int = None,
    start_date: str = None,  # Change to string
    end_date: str = None  # Change to string
):

    query = db.query(models.StockMovement)
    
    if store_id:
        query = query.filter(models.StockMovement.store_id == store_id)
    if product_id:
        query = query.filter(models.StockMovement.product_id == product_id)
    if start_date and end_date:
        # Convert string to datetime objects
        try:
            def parse_date(date_str):
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            query = query.filter(models.StockMovement.timestamp.between(start_date, end_date))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")
    
    return query.all()



# @app.put("/products/{product_id}", response_model=schemas.Product)
# def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
#     db_product = crud.update_product(db=db, product_id=product_id, product=product)
#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product

# Endpoint to delete a product
# @app.delete("/products/{product_id}", response_model=schemas.Product)
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     db_product = crud.delete_product(db=db, product_id=product_id)
#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product


# @app.put("/stock-movements/{movement_id}", response_model=schemas.StockMovement)
# def update_stock_movement(movement_id: int, movement: schemas.StockMovementCreate, db: Session = Depends(get_db)):
#     db_movement = crud.update_stock_movement(db=db, movement_id=movement_id, movement=movement)
#     if not db_movement:
#         raise HTTPException(status_code=404, detail="Stock movement not found")
#     return db_movement

# Endpoint to delete a stock movement
# @app.delete("/stock-movements/{movement_id}", response_model=schemas.StockMovement)
# def delete_stock_movement(movement_id: int, db: Session = Depends(get_db)):
#     db_movement = crud.delete_stock_movement(db=db, movement_id=movement_id)
#     if not db_movement:
#         raise HTTPException(status_code=404, detail="Stock movement not found")
#     return db_movement

@app.post("/stores/")
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)  
    db_store = crud.create_store(db, store)

    crud.create_audit_log(
        db=db,
        username=credentials.username,
        action="CREATE_STORE",
        target_table="stores",
        target_id=db_store.id,
        details=f"Created store '{store.name}'"
    )

    return db_store




@app.get("/stores/", response_model=List[schemas.Store])
def get_stores(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    return crud.get_stores(db)





@app.get("/products/")
@limiter.limit("10/minute") 
def get_products(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)


# @app.get("/inventory/{store_id}", response_model=list[schemas.InventoryDisplay])
# def get_store_inventory(store_id: int, db: Session = Depends(get_db)):
#     return crud.get_inventory_by_store(db, store_id)

from app.redis_client import redis_client  # ⬅️ ADD THIS at the top of your file

@app.get("/inventory/{store_id}", response_model=list[schemas.InventoryDisplay])
def get_store_inventory(store_id: int, db: Session = Depends(get_db)):
    cache_key = f"inventory:store:{store_id}"
    cached_inventory = redis_client.get(cache_key)

    if cached_inventory:
        print("FROM CACHE")
        import json
        return json.loads(cached_inventory)  # Convert string back to Python list

    inventory = crud.get_inventory_by_store(db, store_id)

    # Save to Redis cache for 60 seconds
    import json
    redis_client.set(cache_key, json.dumps(inventory), ex=60)
    print("FROM DATABASE")
    return inventory


@app.get("/products/{product_id}/inventory", response_model=List[schemas.ProductInventoryDisplay])
def get_product_inventory(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"inventory:product:{product_id}"
    cached_inventory = redis_client.get(cache_key)

    if cached_inventory:
        print("FROM CACHE")
        import json
        return json.loads(cached_inventory)

    inventory = crud.get_inventory_by_product(db, product_id)

    import json
    redis_client.set(cache_key, json.dumps(inventory), ex=60)
    print("FROM DATABASE")
    return inventory
