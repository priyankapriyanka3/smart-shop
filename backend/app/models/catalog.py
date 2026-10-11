"""Catalog domain models: Categories and Products."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    """Product category with hierarchical support."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    status = Column(String(50), nullable=False, default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")


class Product(Base):
    """Product catalog item."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    sku = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(500), nullable=False)
    slug = Column(String(500), nullable=False, unique=True, index=True)
    brand = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String(1000), nullable=True)
    status = Column(String(50), nullable=False, default="active")  # active, inactive, discontinued
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    inventory_records = relationship("Inventory", back_populates="product")
    reviews = relationship("Review", back_populates="product")


# Indexes for performance
Index("idx_product_category", Product.category_id)
Index("idx_product_status", Product.status)
