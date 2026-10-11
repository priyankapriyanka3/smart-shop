"""Supplier schemas for request/response models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierCreate(BaseModel):
    """Supplier creation request."""
    name: str = Field(..., min_length=1, max_length=100)
    contact_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    country: str | None = Field(None, max_length=50)
    website: str | None = Field(None, max_length=200)
    lead_time_days: int = Field(..., gt=0, le=365)
    rating: int | None = Field(None, ge=1, le=5)


class SupplierUpdate(BaseModel):
    """Supplier update request."""
    name: str | None = Field(None, min_length=1, max_length=100)
    contact_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    country: str | None = Field(None, max_length=50)
    website: str | None = Field(None, max_length=200)
    lead_time_days: int | None = Field(None, gt=0, le=365)
    rating: int | None = Field(None, ge=1, le=5)


class SupplierResponse(BaseModel):
    """Supplier response model."""
    id: int
    name: str
    contact_name: str
    email: str
    phone: str | None = None
    country: str | None = None
    website: str | None = None
    lead_time_days: int
    rating: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
