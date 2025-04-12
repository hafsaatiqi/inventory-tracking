from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_stock_movements(db: Session):
    return db.query(models.StockMovement).all()

# def get_stock_movements(db: Session):
#     return db.query(models.StockMovement).all()

# Update a product's details
def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Only update fields that are not None
    if product.name is not None:
        db_product.name = product.name
    if product.price is not None:
        db_product.price = product.price
    # if product.quantity is not None:
    #     db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product


# Update a stock movement (if applicable)
def update_stock_movement(db: Session, movement_id: int, movement: schemas.StockMovementCreate):
    # Fetch the existing stock movement
    db_movement = db.query(models.StockMovement).filter(models.StockMovement.id == movement_id).first()
    
    if not db_movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    
    # Only update the fields that are provided (not None)
    if movement.quantity is not None:
        db_movement.quantity = movement.quantity
    if movement.type is not None:
        db_movement.type = movement.type

    db.commit()
    db.refresh(db_movement)
    return db_movement


# Delete a product
def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

# Delete a stock movement
def delete_stock_movement(db: Session, movement_id: int):
    movement = db.query(models.StockMovement).filter(models.StockMovement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")

    db.delete(movement)
    db.commit()
    return {"detail": "Stock movement deleted successfully"}


def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(name=store.name)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_stores(db: Session):
    return db.query(models.Store).all()


from sqlalchemy.exc import SQLAlchemyError

def create_stock_movement(db: Session, movement: schemas.StockMovementCreate):
    try:
        # Verify product and store exist
        if not db.query(models.Product).filter_by(id=movement.product_id).first():
            raise HTTPException(status_code=404, detail="Product not found")
        if not db.query(models.Store).filter_by(id=movement.store_id).first():
            raise HTTPException(status_code=404, detail="Store not found")

        # Handle inventory update
        inventory = db.query(models.StoreInventory).filter_by(
            store_id=movement.store_id,
            product_id=movement.product_id
        ).with_for_update().first()

        if not inventory:
            inventory = models.StoreInventory(
                store_id=movement.store_id,
                product_id=movement.product_id,
                quantity=0
            )
            db.add(inventory)
            db.flush()

        # Update quantity based on movement type
        if movement.type == "stock_in":
            inventory.quantity += movement.quantity
        elif movement.type in ["sale", "manual_removal"]:
            if inventory.quantity < movement.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")
            inventory.quantity -= movement.quantity

        # Create the movement record (let SQLAlchemy handle created_at)
        db_movement = models.StockMovement(
            product_id=movement.product_id,
            store_id=movement.store_id,
            type=movement.type,
            quantity=movement.quantity
        )
        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        return db_movement

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_inventory_by_store(db: Session, store_id: int):
    inventory = db.query(models.StoreInventory).filter(models.StoreInventory.store_id == store_id).all()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="No inventory found for this store")

    result = []
    for item in inventory:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        result.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "quantity": item.quantity
        })
    return result


def get_inventory_by_product(db: Session, product_id: int):
    """Get current inventory levels for a product across all stores"""
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get inventory across all stores
    inventory = db.query(models.StoreInventory).filter(
        models.StoreInventory.product_id == product_id
    ).all()
    
    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="No inventory found for this product in any store"
        )
    
    result = []
    for item in inventory:
        store = db.query(models.Store).filter(models.Store.id == item.store_id).first()
        result.append({
            "store_id": item.store_id,
            "store_name": store.name,
            "product_id": item.product_id,
            "product_name": product.name,
            "quantity": item.quantity
        })
    
    return result