from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.inventory import InventoryItemResponse, InventoryItemCreate, StockMovementResponse, StockMovementCreate
from app.crud import inventory as crud_inventory

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/items", response_model=list[InventoryItemResponse])
def list_items(db: Session = Depends(get_db)):
    """List all inventory items"""
    return crud_inventory.get_ingredients(db)

@router.post("/items", response_model=InventoryItemResponse)
def create_item(item: InventoryItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    return crud_inventory.create_ingredient(db, item)

@router.get("/items/{item_id}", response_model=InventoryItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific inventory item"""
    item = crud_inventory.get_ingredient(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=InventoryItemResponse)
def update_item(item_id: int, item: InventoryItemCreate, db: Session = Depends(get_db)):
    """Update an inventory item"""
    updated = crud_inventory.update_ingredient(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an inventory item"""
    deleted = crud_inventory.delete_ingredient(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}

@router.get("/items/low-stock", response_model=list[InventoryItemResponse])
def get_low_stock_items(db: Session = Depends(get_db)):
    """Get items with low stock"""
    return crud_inventory.get_low_stock_items(db)

@router.post("/movements", response_model=StockMovementResponse)
def create_stock_movement(movement: StockMovementCreate, db: Session = Depends(get_db)):
    """Record a stock movement"""
    result = crud_inventory.create_stock_movement(db, movement)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@router.get("/movements", response_model=list[StockMovementResponse])
def list_movements(ingredient_id: int = None, db: Session = Depends(get_db)):
    """List stock movements"""
    return crud_inventory.get_stock_movements(db, ingredient_id)
