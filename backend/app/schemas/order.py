"""Order schemas for request/response models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemResponse(BaseModel):
    """Order item response model."""
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product_name: str | None = None
    product_brand: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    """Order response model."""
    id: int
    customer_id: int
    order_date: datetime
    total_amount: Decimal
    status: str
    delivery_address: str | None = None
    discount_code: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    """Order status update request."""
    status: str = Field(..., pattern="^(pending|confirmed|shipped|delivered)$")


class OrderNoteCreate(BaseModel):
    """Order note creation request."""
    note: str = Field(..., min_length=1, max_length=500)
