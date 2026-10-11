"""Inventory domain models: Warehouses, Suppliers, and Inventory records."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Warehouse(Base):
    """Warehouse or fulfillment location."""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True, index=True)
    location = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    inventory_records = relationship("Inventory", back_populates="warehouse")


class Supplier(Base):
    """Product supplier."""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True, index=True)
    contact_email = Column(String(255), nullable=True)
    lead_time_days = Column(Integer, nullable=False, default=7)
    status = Column(String(50), nullable=False, default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    inventory_records = relationship("Inventory", back_populates="supplier")


class Inventory(Base):
    """Product inventory record per warehouse."""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=10)
    status = Column(String(50), nullable=False, default="in_stock")  # in_stock, low_stock, out_of_stock
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_records")
    warehouse = relationship("Warehouse", back_populates="inventory_records")
    supplier = relationship("Supplier", back_populates="inventory_records")


# Indexes for performance
Index("idx_inventory_product", Inventory.product_id)
Index("idx_inventory_warehouse", Inventory.warehouse_id)
Index("idx_inventory_status", Inventory.status)
