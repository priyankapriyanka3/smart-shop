"""Payments domain service: Payment state tracking."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.payments import Payment
from app.schemas.payments import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
)


class PaymentService:
    """Service for payment operations."""

    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, data: PaymentCreate) -> PaymentResponse:
        """Create payment record."""
        payment = Payment(**data.model_dump())
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return PaymentResponse.model_validate(payment)

    def get_payment_by_id(self, payment_id: int) -> Optional[PaymentResponse]:
        """Get payment by ID."""
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        return PaymentResponse.model_validate(payment) if payment else None

    def get_payments_by_order(self, order_id: int) -> list[PaymentResponse]:
        """Get all payments for an order."""
        payments = self.db.query(Payment).filter(Payment.order_id == order_id).all()
        return [PaymentResponse.model_validate(p) for p in payments]

    def update_payment_status(
        self,
        payment_id: int,
        data: PaymentStatusUpdate,
    ) -> Optional[PaymentResponse]:
        """Update payment status."""
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(payment, key, value)

        self.db.commit()
        self.db.refresh(payment)
        return PaymentResponse.model_validate(payment)

    def authorize_payment(
        self,
        order_id: int,
        amount: float,
        payment_method: str,
    ) -> PaymentResponse:
        """Authorize payment (mock for Phase 1)."""
        # Mock authorization - always succeeds for now
        payment_data = PaymentCreate(
            order_id=order_id,
            amount=amount,
            currency="USD",
            payment_method=payment_method,
            status="authorized",
            external_reference=f"MOCK-{order_id}",
        )
        return self.create_payment(payment_data)
