from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime 

class ProductCreate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    # quantity: Optional[int] = None

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
    type: str = Field(..., pattern="^(stock_in|sale|manual_removal)$")
    quantity: int
    # timestamp: Optional[datetime] = None  # ← Add this

class StockMovement(StockMovementCreate):
    id: int
    created_at: datetime  # Add this to match the model
    class Config:
        orm_mode = True


from pydantic import BaseModel

class InventoryDisplay(BaseModel):
    # store_id: int
    # store_name: str
    product_id: int
    product_name: str
    quantity: int

    class Config:
        orm_mode = True

class ProductInventoryDisplay(BaseModel):
    store_id: int
    store_name: str
    product_id: int
    product_name: str
    quantity: int

    class Config:
        orm_mode = True


class AuditLog(BaseModel):
    id: int
    username: str
    action: str
    target_table: str
    target_id: int | None = None
    details: str | None = None
    timestamp: datetime

    class Config:
        orm_mode = True
