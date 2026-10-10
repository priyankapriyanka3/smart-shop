"""Product model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    """Product catalog item."""

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    brand = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    is_active = Column(String(32), nullable=False, default="draft")  # draft, active, inactive
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    inventory_records = relationship("Inventory", back_populates="product")
    reviews = relationship("Review", back_populates="product")

    # Indexes
    __table_args__ = (
        Index("idx_product_is_active_category", "is_active", "category_id"),
        Index("idx_product_brand", "brand"),
    )
