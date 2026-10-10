"""Supplier schemas for request/response models."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class SupplierCreate(BaseModel):
    """Supplier creation request."""
    name: str = Field(..., min_length=1, max_length=100)
    contact_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=200)
    lead_time_days: int = Field(..., gt=0, le=365)
    rating: Optional[int] = Field(None, ge=1, le=5)


class SupplierUpdate(BaseModel):
    """Supplier update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    contact_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=200)
    lead_time_days: Optional[int] = Field(None, gt=0, le=365)
    rating: Optional[int] = Field(None, ge=1, le=5)


class SupplierResponse(BaseModel):
    """Supplier response model."""
    id: int
    name: str
    contact_name: str
    email: str
    phone: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    lead_time_days: int
    rating: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
