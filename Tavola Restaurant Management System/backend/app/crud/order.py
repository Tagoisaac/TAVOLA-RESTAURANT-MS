from sqlalchemy.orm import Session
from app.db.models.order import Table, Order, OrderItem, Payment
from app.schemas.order import TableCreate, OrderCreate, OrderStatusUpdate, PaymentCreate
import uuid

def get_tables(db: Session):
    return db.query(Table).all()

def get_table(db: Session, table_id: int):
    return db.query(Table).filter(Table.id == table_id).first()

def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, order: OrderCreate):
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    db_order = Order(
        order_number=order_number,
        table_id=order.table_id,
        order_type=order.order_type,
        status="pending",
    )
    db.add(db_order)
    db.flush()
    
    # Add order items
    total_amount = 0.0
    for item_data in order.items:
        order_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            special_instructions=item_data.special_instructions,
        )
        db.add(order_item)
        # Calculate item total (would fetch from MenuItem in real scenario)
        # For now, using a placeholder
        total_amount += item_data.quantity * 10.0  # Placeholder
    
    db_order.total_amount = total_amount
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status_update: OrderStatusUpdate):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status_update.status
        db.commit()
        db.refresh(db_order)
    return db_order

def get_payments(db: Session):
    return db.query(Payment).all()

def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        transaction_id=payment.transaction_id,
        status="completed",
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def refund_payment(db: Session, payment_id: int):
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db_payment.status = "refunded"
        # Update order status back to pending
        order = get_order(db, db_payment.order_id)
        if order:
            order.status = "pending"
        db.commit()
        db.refresh(db_payment)
    return db_payment
