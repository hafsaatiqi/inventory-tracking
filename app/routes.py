from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter()

@router.post("/stock-movements/")
def create_stock_movement(movement: schemas.StockMovementCreate, db: Session = Depends(get_db)):
    return crud.create_stock_movement(db, movement)

@router.get("/stock-movements/")
def get_all_movements(db: Session = Depends(get_db)):
    return crud.get_stock_movements(db)

@router.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Hello!"}

