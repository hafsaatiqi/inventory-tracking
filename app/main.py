from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
import app.models
import app.crud
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
    return app.crud.create_product(db, product)

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return app.crud.get_products(db)
