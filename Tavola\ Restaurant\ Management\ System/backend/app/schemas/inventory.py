from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupplierCreate(BaseModel):
    name: str
    contact_person: str
    email: str
    phone: str
    address: Optional[str] = None

class SupplierResponse(SupplierCreate):
    id: int

    class Config:
        from_attributes = True

class InventoryItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    unit: str
    current_stock: float = 0
    min_stock_level: float = 0
    supplier_id: Optional[int] = None

class InventoryItemResponse(InventoryItemCreate):
    id: int

    class Config:
        from_attributes = True

class StockMovementCreate(BaseModel):
    ingredient_id: int
    quantity: float
    movement_type: str  # purchase, consumption, adjustment, waste
    reference_id: Optional[int] = None
    notes: Optional[str] = None

class StockMovementResponse(StockMovementCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
