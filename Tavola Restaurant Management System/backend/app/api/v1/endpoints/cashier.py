from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import PaymentResponse, PaymentCreate
from app.crud import order as crud_order

router = APIRouter(prefix="/cashier", tags=["cashier"])

@router.get("/orders/{order_id}/invoice")
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    """Generate invoice for an order"""
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "order_id": order.id,
        "order_number": order.order_number,
        "items": order.items if hasattr(order, 'items') else [],
        "subtotal": order.total_amount,
        "tax_amount": order.total_amount * 0.10,  # 10% tax
        "total_amount": order.total_amount * 1.10,
    }

@router.post("/payments", response_model=PaymentResponse)
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Process a payment for an order"""
    order = crud_order.get_order(db, payment.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Validate amount
    expected_amount = order.total_amount * 1.10  # With tax
    if payment.amount != expected_amount and payment.amount != order.total_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Payment amount mismatch. Expected {expected_amount}"
        )
    
    # Create payment
    return crud_order.create_payment(db, payment)

@router.post("/payments/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    """Refund a payment"""
    refunded = crud_order.refund_payment(db, payment_id)
    if not refunded:
        raise HTTPException(status_code=404, detail="Payment not found")
    return refunded

@router.get("/payments", response_model=list[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    """List all payments"""
    return crud_order.get_payments(db)
