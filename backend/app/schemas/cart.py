"""Cart schemas."""
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CartItemBase(BaseModel):
    """Base cart item schema."""

    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    """Cart item creation schema."""

    pass


class CartItemUpdate(BaseModel):
    """Cart item update schema."""

    quantity: int = Field(..., gt=0)


class ProductSummary(BaseModel):
    """Product summary for cart items."""

    id: int
    name: str
    brand: str
    price: Decimal
    sku: str
    stock_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CartItemResponse(BaseModel):
    """Cart item response schema."""

    id: int
    cart_id: int
    product_id: int
    quantity: int
    product: ProductSummary
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    """Cart response schema."""

    id: int
    customer_id: int
    items: List[CartItemResponse]
    total_items: int
    subtotal: Decimal
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
