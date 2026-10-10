"""Inventory schemas for request/response models."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class InventoryResponse(BaseModel):
    """Inventory response model."""
    id: int
    product_id: int
    warehouse_id: int
    quantity: int
    reorder_level: int
    last_updated: datetime
    created_at: datetime
    updated_at: datetime
    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    warehouse_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InventoryUpdate(BaseModel):
    """Inventory update request."""
    quantity: int = Field(..., ge=0, description="New stock quantity")


class LowStockItem(BaseModel):
    """Low stock item response."""
    id: int
    product_id: int
    product_name: str
    product_sku: str
    warehouse_id: int
    warehouse_name: str
    current_quantity: int
    reorder_level: int
    supplier_name: Optional[str] = None
    supplier_lead_time_days: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
