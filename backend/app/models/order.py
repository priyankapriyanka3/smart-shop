"""Order model for customer orders."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    """Customer order."""

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(64), nullable=False, default="pending")  # pending, confirmed, shipped, delivered
    delivery_address = Column(Text, nullable=True)
    discount_code = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_order_customer_created", "customer_id", "created_at"),
    )
