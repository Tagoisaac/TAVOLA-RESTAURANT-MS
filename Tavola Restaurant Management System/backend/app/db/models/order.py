from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel

class Table(BaseModel):
    __tablename__ = "table"
    
    table_number = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, default="available")  # available, occupied, reserved, cleaning
    
    # Relationships
    orders = relationship("Order", back_populates="table")

class Order(BaseModel):
    __tablename__ = "order"
    
    ORDER_STATUSES = ["pending", "confirmed", "preparing", "ready", "served", "completed", "cancelled"]
    
    order_number = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="pending", nullable=False)
    order_type = Column(String, nullable=False)  # dine-in, takeaway, delivery
    notes = Column(String)
    
    # Foreign Keys
    table_id = Column(Integer, ForeignKey("table.id"), nullable=True)  # Null for takeaway/delivery
    waiter_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    
    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)
    
    @property
    def tax_amount(self):
        # Assuming 10% tax for example
        return self.subtotal * 0.1
    
    @property
    def total_amount(self):
        return self.subtotal + self.tax_amount

class OrderItem(BaseModel):
    __tablename__ = "order_item"
    
    ITEM_STATUSES = ["pending", "preparing", "ready", "served", "cancelled"]
    
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    notes = Column(String)
    status = Column(String, default="pending", nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
    
    @property
    def subtotal(self):
        return self.quantity * self.unit_price

class Payment(BaseModel):
    __tablename__ = "payment"
    
    PAYMENT_METHODS = ["cash", "credit_card", "debit_card", "mobile_payment"]
    PAYMENT_STATUSES = ["pending", "completed", "failed", "refunded"]
    
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
    transaction_id = Column(String, unique=True, nullable=True)
    notes = Column(String)
    
    # Relationships
    order = relationship("Order", back_populates="payments")

class Reservation(BaseModel):
    __tablename__ = "reservation"
    
    STATUS_CHOICES = ["confirmed", "seated", "completed", "cancelled", "no_show"]
    
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String)
    reservation_time = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)
    status = Column(String, default="confirmed", nullable=False)
    notes = Column(String)
    
    # Foreign Keys
    table_id = Column(Integer, ForeignKey("table.id"), nullable=True)
    
    # Relationships
    table = relationship("Table")
