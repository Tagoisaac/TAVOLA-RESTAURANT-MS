from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.session import get_db
from app.schemas import InventoryItemResponse, StockMovementCreate, StockMovementResponse
from app.crud import inventory as crud_inventory

router = APIRouter(prefix=f"{settings.API_V1_STR}/inventory", tags=["inventory"])

# Inventory Item Endpoints
@router.get("/items", response_model=List[InventoryItemResponse])
def list_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all inventory items"""
    items = crud_inventory.get_inventory_items(db, skip, limit)
    return items

@router.post("/items", response_model=InventoryItemResponse)
def create_inventory_item(item_data: dict, db: Session = Depends(get_db)):
    """Create inventory item"""
    item = crud_inventory.create_inventory_item(
        db,
        item_data.get("name"),
        item_data.get("unit"),
        item_data.get("current_stock", 0),
        item_data.get("min_stock_level", 0),
        item_data.get("description")
    )
    return item

@router.get("/items/{item_id}", response_model=InventoryItemResponse)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Get inventory item"""
    item = crud_inventory.get_inventory_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(item_id: int, item_data: dict, db: Session = Depends(get_db)):
    """Update inventory item"""
    item = crud_inventory.update_inventory_item(db, item_id, **item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/items/{item_id}")
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Delete inventory item"""
    item = crud_inventory.delete_inventory_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# Stock Movement Endpoints
@router.post("/movements", response_model=StockMovementResponse)
def create_stock_movement(movement_data: StockMovementCreate, db: Session = Depends(get_db)):
    """Record stock movement"""
    movement = crud_inventory.create_stock_movement(
        db,
        movement_data.ingredient_id,
        movement_data.quantity,
        movement_data.movement_type,
        movement_data.reference_id,
        movement_data.notes
    )
    return movement

@router.get("/movements", response_model=List[StockMovementResponse])
def list_stock_movements(ingredient_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get stock movements, optionally filtered by ingredient"""
    movements = crud_inventory.get_stock_movements(db, ingredient_id, skip, limit)
    return movements

@router.get("/low-stock")
def get_low_stock_items(db: Session = Depends(get_db)):
    """Get items below minimum stock level"""
    items = crud_inventory.get_low_stock_items(db)
    return [
        {
            "id": item.id,
            "name": item.name,
            "current_stock": item.current_stock,
            "min_stock_level": item.min_stock_level,
            "unit": item.unit
        }
        for item in items
    ]
