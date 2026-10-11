"""Orders domain schemas: Orders and order items."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)


class OrderItemResponse(OrderItemBase):
    """Order item response with product details."""
    id: int
    order_id: int
    product_name: str
    product_sku: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    """Base order schema."""
    customer_id: int = Field(..., gt=0)
    subtotal: float = Field(..., ge=0)
    discount_amount: float = Field(default=0.0, ge=0)
    shipping_cost: float = Field(default=0.0, ge=0)
    total: float = Field(..., gt=0)
    shipping_street: str = Field(..., min_length=1, max_length=500)
    shipping_city: str = Field(..., min_length=1, max_length=255)
    shipping_state_province: str = Field(..., min_length=1, max_length=255)
    shipping_postal_code: str = Field(..., min_length=1, max_length=50)
    shipping_country: str = Field(..., min_length=1, max_length=100)
    billing_street: str = Field(..., min_length=1, max_length=500)
    billing_city: str = Field(..., min_length=1, max_length=255)
    billing_state_province: str = Field(..., min_length=1, max_length=255)
    billing_postal_code: str = Field(..., min_length=1, max_length=50)
    billing_country: str = Field(..., min_length=1, max_length=100)
    promotion_code: Optional[str] = Field(None, max_length=100)


class OrderCreate(OrderBase):
    """Order creation request."""
    pass


class OrderResponse(OrderBase):
    """Order response with items."""
    id: int
    order_number: str
    status: str
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    """Paginated order list response."""
    items: List[OrderResponse]
    total: int
    page: int
    page_size: int


class OrderStatusUpdate(BaseModel):
    """Order status update request."""
    status: str = Field(..., pattern="^(placed|processing|shipped|delivered|cancelled)$")


class OrderDetailResponse(OrderResponse):
    """Detailed order response with payment information."""
    payment_status: str = "pending"
    payment_method: str = ""
