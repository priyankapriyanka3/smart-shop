"""Discount schemas for request/response models."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class DiscountCreate(BaseModel):
    """Discount creation request."""
    code: str = Field(..., min_length=3, max_length=20, pattern="^[A-Z0-9]+$")
    discount_type: str = Field(..., pattern="^(percentage|fixed_amount)$")
    discount_value: Decimal = Field(..., gt=0)
    min_order_amount: Optional[Decimal] = Field(None, ge=0)
    valid_from: datetime
    valid_to: datetime
    max_uses: Optional[int] = Field(None, gt=0)
    is_active: bool = True


class DiscountUpdate(BaseModel):
    """Discount update request."""
    discount_type: Optional[str] = Field(None, pattern="^(percentage|fixed_amount)$")
    discount_value: Optional[Decimal] = Field(None, gt=0)
    min_order_amount: Optional[Decimal] = Field(None, ge=0)
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    max_uses: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class DiscountResponse(BaseModel):
    """Discount response model."""
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_amount: Optional[Decimal] = None
    valid_from: datetime
    valid_to: datetime
    max_uses: Optional[int] = None
    times_used: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiscountValidationRequest(BaseModel):
    """Discount validation request."""
    code: str = Field(..., min_length=3, max_length=20)
    cart_total: Decimal = Field(..., gt=0)


class DiscountValidationResponse(BaseModel):
    """Discount validation response."""
    valid: bool
    discount_id: Optional[int] = None
    discount_value: Optional[Decimal] = None
    discount_type: Optional[str] = None
    error: Optional[str] = None
