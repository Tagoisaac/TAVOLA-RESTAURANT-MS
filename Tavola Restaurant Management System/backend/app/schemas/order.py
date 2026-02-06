from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TableResponse(BaseModel):
    id: int
    table_number: int
    capacity: int
    location: Optional[str] = None
    status: str = "available"

    class Config:
        from_attributes = True

class TableCreate(BaseModel):
    table_number: int
    capacity: int
    location: Optional[str] = None

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None
    item_total: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    table_id: Optional[int] = None
    order_type: str = "dine_in"
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    order_number: str
    table_id: Optional[int] = None
    order_type: str
    status: str = "pending"
    items: List[OrderItemResponse] = []
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    transaction_id: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str = "completed"
    transaction_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
