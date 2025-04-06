from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class StockMovementCreate(BaseModel):
    product_id: int
    quantity: Optional[int] = None  # Optional for update
    type: Optional[str] = None      # Optional for update

class StockMovement(StockMovementCreate):
    id: int

    class Config:
        orm_mode = True

