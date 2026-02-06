from sqlalchemy.orm import Session
from app.db import models
from typing import Optional

# Inventory Item CRUD
def get_inventory_item(db: Session, item_id: int):
    return db.query(models.Ingredient).filter(models.Ingredient.id == item_id).first()

def get_inventory_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()

def create_inventory_item(db: Session, name: str, unit: str, current_stock: float = 0, 
                         min_stock_level: float = 0, description: Optional[str] = None):
    db_item = models.Ingredient(
        name=name,
        unit=unit,
        current_stock=current_stock,
        min_stock_level=min_stock_level,
        description=description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_inventory_item(db: Session, item_id: int, **kwargs):
    item = get_inventory_item(db, item_id)
    if item:
        for key, value in kwargs.items():
            if value is not None:
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_inventory_item(db: Session, item_id: int):
    item = get_inventory_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item

# Stock Movement CRUD
def create_stock_movement(db: Session, ingredient_id: int, quantity: float, movement_type: str,
                         reference_id: Optional[int] = None, notes: Optional[str] = None):
    # Update ingredient stock
    ingredient = get_inventory_item(db, ingredient_id)
    if ingredient:
        ingredient.current_stock += quantity
        
    db_movement = models.StockMovement(
        ingredient_id=ingredient_id,
        quantity=quantity,
        movement_type=movement_type,
        reference_id=reference_id,
        notes=notes
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_stock_movements(db: Session, ingredient_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.StockMovement)
    if ingredient_id:
        query = query.filter(models.StockMovement.ingredient_id == ingredient_id)
    return query.offset(skip).limit(limit).all()

# Supplier CRUD (Note: Supplier model not in models yet, will add simple version)
def get_low_stock_items(db: Session):
    """Get items that are below minimum stock level"""
    return db.query(models.Ingredient).filter(
        models.Ingredient.current_stock <= models.Ingredient.min_stock_level
    ).all()
