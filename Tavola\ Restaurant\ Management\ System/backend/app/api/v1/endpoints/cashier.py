from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.session import get_db
from app.schemas import PaymentCreate, PaymentResponse
from app.crud import order as crud_order

router = APIRouter(prefix=f"{settings.API_V1_STR}/cashier", tags=["cashier"])

@router.get("/orders/{order_id}/invoice")
def get_invoice(order_id: int, db: Session = Depends(get_db)):
    """Get invoice for an order"""
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    invoice = {
        "order_id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "subtotal": order.subtotal,
        "tax_amount": order.tax_amount,
        "total_amount": order.total_amount,
        "items": [
            {
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            }
            for item in order.items
        ]
    }
    return invoice

@router.post("/payments", response_model=PaymentResponse)
def process_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    """Process payment for an order"""
    order = crud_order.get_order(db, payment_data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Validate payment amount
    if payment_data.amount != order.total_amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Payment amount mismatch. Expected: {order.total_amount}, Received: {payment_data.amount}"
        )
    
    payment = crud_order.create_payment(
        db,
        payment_data.order_id,
        payment_data.amount,
        payment_data.payment_method,
        payment_data.transaction_id,
        payment_data.notes
    )
    
    # Update order and payment status to completed
    crud_order.update_order_status(db, order.id, "completed")
    crud_order.update_payment_status(db, payment.id, "completed")
    
    return payment

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get payment details"""
    payment = crud_order.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/orders/{order_id}/payments")
def get_order_payments(order_id: int, db: Session = Depends(get_db)):
    """Get all payments for an order"""
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    payments = crud_order.get_payments_by_order(db, order_id)
    return payments

@router.post("/payments/{payment_id}/refund")
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    """Refund a payment"""
    payment = crud_order.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    crud_order.update_payment_status(db, payment_id, "refunded")
    
    # Revert order status to pending
    crud_order.update_order_status(db, payment.order_id, "pending")
    
    return {"message": "Payment refunded successfully"}
