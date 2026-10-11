"""Customer model for user accounts."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    """Customer account."""

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(32), default="shopper", nullable=False)  # shopper, admin, inventory_manager, customer_support
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    carts = relationship("Cart", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    audit_logs = relationship("AuditLog", back_populates="actor")
