from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    movements = relationship("StockMovement", back_populates="product")
    inventories = relationship("StoreInventory", back_populates="product")

# class StockMovement(Base):
#     __tablename__ = "stock_movements"

#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     type = Column(String)  # "stock_in", "sale", "manual_removal"
#     quantity = Column(Integer)

#     product = relationship("Product")


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    inventories = relationship("StoreInventory", back_populates="store")
    movements = relationship("StockMovement", back_populates="store")


class StoreInventory(Base):
    __tablename__ = "store_inventory"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)

    store = relationship("Store", back_populates="inventories")
    # product = relationship("Product")
    product = relationship("Product", back_populates="inventories")


class StockMovement(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    type = Column(String, nullable=False)  # stock_in, sale, manual_removal
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="movements")
    store = relationship("Store", back_populates="movements")
