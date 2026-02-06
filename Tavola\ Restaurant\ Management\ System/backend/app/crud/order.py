from sqlalchemy.orm import Session
from app.db import models
from typing import Optional, List
from datetime import datetime

# Table CRUD
def get_table(db: Session, table_id: int):
    return db.query(models.Table).filter(models.Table.id == table_id).first()

def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Table).offset(skip).limit(limit).all()

def create_table(db: Session, table_number: str, capacity: int):
    db_table = models.Table(table_number=table_number, capacity=capacity)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def update_table(db: Session, table_id: int, **kwargs):
    table = get_table(db, table_id)
    if table:
        for key, value in kwargs.items():
            if value is not None:
                setattr(table, key, value)
        db.commit()
        db.refresh(table)
    return table

def delete_table(db: Session, table_id: int):
    table = get_table(db, table_id)
    if table:
        db.delete(table)
        db.commit()
    return table

# Order CRUD
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order_number: str, order_type: str, table_id: Optional[int] = None, notes: Optional[str] = None):
    db_order = models.Order(
        order_number=order_number,
        order_type=order_type,
        table_id=table_id,
        notes=notes
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: str):
    order = get_order(db, order_id)
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order

# OrderItem CRUD
def create_order_item(db: Session, order_id: int, menu_item_id: int, quantity: int, unit_price: float, notes: Optional[str] = None):
    db_item = models.OrderItem(
        order_id=order_id,
        menu_item_id=menu_item_id,
        quantity=quantity,
        unit_price=unit_price,
        notes=notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_order_item_status(db: Session, item_id: int, status: str):
    item = db.query(models.OrderItem).filter(models.OrderItem.id == item_id).first()
    if item:
        item.status = status
        db.commit()
        db.refresh(item)
    return item

# Payment CRUD
def create_payment(db: Session, order_id: int, amount: float, payment_method: str, 
                  transaction_id: Optional[str] = None, notes: Optional[str] = None):
    db_payment = models.Payment(
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id,
        notes=notes,
        status="pending"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment_status(db: Session, payment_id: int, status: str):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_payments_by_order(db: Session, order_id: int):
    return db.query(models.Payment).filter(models.Payment.order_id == order_id).all()
