"""Product schemas."""
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Base product schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    brand: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: int = Field(..., gt=0)


class ProductCreate(ProductBase):
    """Product creation schema."""

    pass


class ProductUpdate(BaseModel):
    """Product update schema - all fields optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    brand: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category_id: Optional[int] = Field(None, gt=0)


class ProductResponse(ProductBase):
    """Product response schema."""

    id: int
    is_active: str
    stock_status: Optional[str] = None  # Computed: in_stock, low_stock, out_of_stock
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
