"""Customer domain models: Users and Addresses."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """Customer or internal user account."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, inactive, suspended
    consent_timestamp = Column(DateTime, nullable=True)  # GDPR consent tracking
    is_deleted = Column(Boolean, nullable=False, default=False)  # Soft delete for GDPR
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    addresses = relationship("Address", back_populates="user")
    carts = relationship("Cart", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    user_roles = relationship("UserRole", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="AuditLog.user_id")


class Address(Base):
    """Customer shipping or billing address."""
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_type = Column(String(50), nullable=False)  # shipping, billing
    street = Column(String(500), nullable=False)
    city = Column(String(255), nullable=False)
    state_province = Column(String(255), nullable=False)
    postal_code = Column(String(50), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="addresses")


# Indexes for performance
Index("idx_address_user", Address.user_id)
