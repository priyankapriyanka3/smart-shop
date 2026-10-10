"""Supplier model for product suppliers."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Supplier(Base):
    """Product supplier."""

    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    email = Column(String(320), nullable=False)
    phone = Column(String(40), nullable=True)
    country = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    lead_time_days = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
