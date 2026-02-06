from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TableCreate(BaseModel):
    table_number: str
    capacity: int

class TableResponse(TableCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    unit_price: float
    notes: Optional[str] = None

class OrderItemResponse(OrderItemCreate):
    id: int
    order_id: int
    status: str

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    order_type: str  # dine-in, takeaway, delivery
    table_id: Optional[int] = None
    notes: Optional[str] = None
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    order_type: str
    notes: Optional[str] = None
    table_id: Optional[int] = None
    subtotal: float
    tax_amount: float
    total_amount: float
    items: List[OrderItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str  # cash, credit_card, debit_card, mobile_payment
    transaction_id: Optional[str] = None
    notes: Optional[str] = None

class PaymentResponse(PaymentCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
