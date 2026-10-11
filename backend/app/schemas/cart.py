"""Cart domain schemas: Shopping carts and cart items."""
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class CartItemBase(BaseModel):
    """Base cart item schema."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    """Cart item creation request."""
    pass


class CartItemUpdate(BaseModel):
    """Cart item update request."""
    quantity: int = Field(..., gt=0)


class AddToCartRequest(BaseModel):
    """Request to add item to cart."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)


class UpdateCartItemRequest(BaseModel):
    """Request to update cart item quantity."""
    quantity: int = Field(..., gt=0)


class CartItemResponse(CartItemBase):
    """Cart item response with product details."""
    id: int
    cart_id: int
    product_name: str
    product_price: float
    product_image_url: str | None
    subtotal: float
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CartBase(BaseModel):
    """Base cart schema."""
    customer_id: int = Field(..., gt=0)
    status: str = Field(default="active", pattern="^(active|abandoned|converted)$")


class CartResponse(CartBase):
    """Cart response with items."""
    id: int
    items: List[CartItemResponse]
    subtotal: float
    total_items: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
