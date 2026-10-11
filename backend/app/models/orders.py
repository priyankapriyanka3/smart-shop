"""Orders domain models: Orders and order items."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    """Customer order."""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_number = Column(String(100), nullable=False, unique=True, index=True)
    status = Column(String(50), nullable=False, default="placed")  # placed, processing, shipped, delivered, cancelled
    subtotal = Column(Float, nullable=False)
    discount_amount = Column(Float, nullable=False, default=0.0)
    shipping_cost = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False)
    
    # Shipping address
    shipping_street = Column(String(500), nullable=False)
    shipping_city = Column(String(255), nullable=False)
    shipping_state_province = Column(String(255), nullable=False)
    shipping_postal_code = Column(String(50), nullable=False)
    shipping_country = Column(String(100), nullable=False)
    
    # Billing address
    billing_street = Column(String(500), nullable=False)
    billing_city = Column(String(255), nullable=False)
    billing_state_province = Column(String(255), nullable=False)
    billing_postal_code = Column(String(50), nullable=False)
    billing_country = Column(String(100), nullable=False)
    
    promotion_code = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")


class OrderItem(Base):
    """Individual item in an order."""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


# Indexes for performance
Index("idx_order_customer", Order.customer_id)
Index("idx_order_status", Order.status)
Index("idx_order_item_order", OrderItem.order_id)
