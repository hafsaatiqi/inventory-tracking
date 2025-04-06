from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
import app.models
from app import crud
from app import schemas

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

@app.get("/")
def read_root():
    return {"message": "Inventory Tracking API"}

@app.post("/products/")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

from typing import List

@app.get("/products/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

# app/main.py
@app.post("/stock-movements/")
async def create_stock_movement(
    movement: schemas.StockMovementCreate,  # This will be passed in the request body
    db: Session = Depends(get_db)  # Database session injected by FastAPI
):
    return crud.create_stock_movement(db=db, movement=movement)

@app.get("/stock-movements/")
def get_stock_movements(db: Session = Depends(get_db)):
    return crud.get_stock_movements(db)


from app.routes import router as inventory_router

app.include_router(inventory_router)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db=db, product_id=product_id, product=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Endpoint to delete a product
@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/stock-movements/{movement_id}", response_model=schemas.StockMovement)
def update_stock_movement(movement_id: int, movement: schemas.StockMovementCreate, db: Session = Depends(get_db)):
    db_movement = crud.update_stock_movement(db=db, movement_id=movement_id, movement=movement)
    if not db_movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return db_movement

# Endpoint to delete a stock movement
@app.delete("/stock-movements/{movement_id}", response_model=schemas.StockMovement)
def delete_stock_movement(movement_id: int, db: Session = Depends(get_db)):
    db_movement = crud.delete_stock_movement(db=db, movement_id=movement_id)
    if not db_movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return db_movement