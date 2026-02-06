from sqlalchemy.orm import Session
from app.db.models.menu import Ingredient, StockMovement
from app.schemas.inventory import InventoryItemCreate, StockMovementCreate

def get_ingredients(db: Session):
    return db.query(Ingredient).all()

def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

def create_ingredient(db: Session, ingredient: InventoryItemCreate):
    db_ingredient = Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def update_ingredient(db: Session, ingredient_id: int, ingredient: InventoryItemCreate):
    db_ingredient = get_ingredient(db, ingredient_id)
    if db_ingredient:
        for key, value in ingredient.dict().items():
            setattr(db_ingredient, key, value)
        db.commit()
        db.refresh(db_ingredient)
    return db_ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = get_ingredient(db, ingredient_id)
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
    return db_ingredient

def get_low_stock_items(db: Session):
    return db.query(Ingredient).filter(
        Ingredient.current_stock < Ingredient.reorder_level
    ).all()

def create_stock_movement(db: Session, movement: StockMovementCreate):
    # Get the ingredient
    ingredient = get_ingredient(db, movement.ingredient_id)
    if not ingredient:
        return None
    
    # Create movement record
    db_movement = StockMovement(**movement.dict())
    db.add(db_movement)
    
    # Update ingredient stock
    ingredient.current_stock += movement.quantity
    
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_stock_movements(db: Session, ingredient_id: int = None):
    query = db.query(StockMovement)
    if ingredient_id:
        query = query.filter(StockMovement.ingredient_id == ingredient_id)
    return query.all()
