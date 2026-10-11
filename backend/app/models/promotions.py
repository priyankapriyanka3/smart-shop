"""Promotions domain models: Discount campaigns and promotion codes."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.database import Base


class Promotion(Base):
    """Promotion or discount campaign."""
    __tablename__ = "promotions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    discount_type = Column(String(50), nullable=False)  # percentage, fixed, free_shipping
    discount_value = Column(Float, nullable=False)
    minimum_order_amount = Column(Float, nullable=False, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    max_uses = Column(Integer, nullable=True)  # NULL for unlimited
    current_uses = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="inactive")  # active, inactive, expired
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Indexes for performance
Index("idx_promotion_status", Promotion.status)
Index("idx_promotion_dates", Promotion.start_date, Promotion.end_date)
