"""Checkout domain schemas."""
from typing import Optional
from pydantic import BaseModel, Field


class CheckoutAddress(BaseModel):
    """Address for checkout."""
    street: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=255)
    state_province: str = Field(..., min_length=1, max_length=255)
    postal_code: str = Field(..., min_length=1, max_length=50)
    country: str = Field(..., min_length=1, max_length=100)


class CheckoutRequest(BaseModel):
    """Checkout request with addresses and payment info."""
    shipping_address: Optional[CheckoutAddress] = None
    billing_address: Optional[CheckoutAddress] = None
    shipping_address_id: Optional[int] = None
    billing_address_id: Optional[int] = None
    payment_method: Optional[str] = Field(None, min_length=1, max_length=100)
    promotion_code: Optional[str] = Field(None, max_length=100)


class CheckoutValidationResponse(BaseModel):
    """Checkout validation response."""
    valid: bool
    errors: list[str] = []
    inventory_issues: list[dict] = []
    promotion_valid: bool = True
    promotion_discount: float = 0.0
    subtotal: float = 0.0
    discount_amount: float = 0.0
    discount: float = 0.0  # Alias for discount_amount for test compatibility
    shipping_cost: float = 0.0
    total: float = 0.0


class CheckoutResponse(BaseModel):
    """Checkout submission response with order ID."""
    order_id: int
    order_number: str
    subtotal: float
    discount_amount: float
    shipping_cost: float
    total: float
    payment_status: str
    message: str = "Order created successfully"
