from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact: Optional[str] = None

    class Config:
        from_attributes = True

class InventoryItemResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: float
    min_stock_level: float
    reorder_level: float

    class Config:
        from_attributes = True

class InventoryItemCreate(BaseModel):
    name: str
    unit: str
    current_stock: float = 0.0
    min_stock_level: float = 0.0
    reorder_level: float = 0.0
    supplier_id: Optional[int] = None

class StockMovementCreate(BaseModel):
    ingredient_id: int
    quantity: float
    movement_type: str
    notes: Optional[str] = None

class StockMovementResponse(BaseModel):
    id: int
    ingredient_id: int
    quantity: float
    movement_type: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
