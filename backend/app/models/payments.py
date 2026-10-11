"""Payments domain models: Payment records."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Payment(Base):
    """Payment record for an order."""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    payment_method = Column(String(100), nullable=False)  # credit_card, paypal, etc.
    status = Column(String(50), nullable=False, default="pending")  # pending, authorized, failed, refunded
    external_reference = Column(String(255), nullable=True)  # Processor-specific reference
    failure_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="payments")


# Indexes for performance
Index("idx_payment_order", Payment.order_id)
Index("idx_payment_status", Payment.status)
