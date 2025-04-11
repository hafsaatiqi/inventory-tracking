from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

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


class StoreInventory(Base):
    __tablename__ = "store_inventory"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)

    store = relationship("Store", back_populates="inventories")
    product = relationship("Product")

# Update your StockMovement to include store_id
class StockMovement(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    type = Column(String)  # stock_in, sale, manual_removal
    quantity = Column(Integer)

    product = relationship("Product")
    store = relationship("Store")
