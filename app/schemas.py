from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class ProductCreate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    class Config:
        orm_mode = True

# Update stock movement
class StockMovementCreate(BaseModel):
    product_id: int
    store_id: int
    type: str
    quantity: int
    timestamp: Optional[datetime] = None  # ← Add this

class StockMovement(StockMovementCreate):
    id: int
    class Config:
        orm_mode = True

