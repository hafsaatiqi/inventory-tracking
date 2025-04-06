from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()


def create_stock_movement(db: Session, movement: schemas.StockMovementCreate):
    # Check if the product exists
    product = db.query(models.Product).filter(models.Product.id == movement.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update stock based on movement type
    if movement.type == "stock_in":
        product.quantity += movement.quantity
    elif movement.type in ["sale", "manual_removal"]:
        if product.quantity < movement.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        product.quantity -= movement.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid movement type")

    # Create stock movement record
    db_movement = models.StockMovement(
        product_id=movement.product_id,
        type=movement.type,
        quantity=movement.quantity
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

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
    if product.quantity is not None:
        db_product.quantity = product.quantity

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
