"""Product schemas."""
from decimal import Decimal

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

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, min_length=1)
    brand: str | None = Field(None, min_length=1, max_length=255)
    sku: str | None = Field(None, min_length=1, max_length=100)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    category_id: int | None = Field(None, gt=0)


class ProductResponse(ProductBase):
    """Product response schema."""

    id: int
    is_active: str
    stock_status: str | None = None  # Computed: in_stock, low_stock, out_of_stock
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
