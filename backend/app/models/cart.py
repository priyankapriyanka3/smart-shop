"""Cart domain models: Shopping carts and cart items."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Cart(Base):
    """Shopping cart for a customer."""
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, abandoned, converted
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    @property
    def subtotal(self) -> float:
        """Calculate cart subtotal from items."""
        return sum(item.product.price * item.quantity for item in self.items)
    
    @property
    def total_items(self) -> int:
        """Count total items in cart."""
        return sum(item.quantity for item in self.items)


class CartItem(Base):
    """Individual item in a shopping cart."""
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")


# Indexes for performance
Index("idx_cart_customer", Cart.customer_id)
Index("idx_cart_item_cart", CartItem.cart_id)
Index("idx_cart_item_product", CartItem.product_id)
