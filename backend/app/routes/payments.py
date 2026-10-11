"""Payment routes: payment status and history."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.payments import PaymentService
from app.schemas.payments import (
    PaymentResponse,
    PaymentListResponse,
)


router = APIRouter()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    """Get payment by ID."""
    service = PaymentService(db)
    payment = service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/order/{order_id}", response_model=PaymentListResponse)
def get_order_payments(
    order_id: int,
    db: Session = Depends(get_db),
):
    """Get all payments for an order."""
    service = PaymentService(db)
    return service.get_payments_by_order(order_id)
