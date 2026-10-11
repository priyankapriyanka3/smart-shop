"""Payments domain schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class PaymentBase(BaseModel):
    """Base payment schema."""
    order_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=10)
    payment_method: str = Field(..., min_length=1, max_length=100)
    status: str = Field(
        default="pending",
        pattern="^(pending|authorized|failed|refunded)$"
    )
    external_reference: Optional[str] = Field(None, max_length=255)
    failure_reason: Optional[str] = Field(None, max_length=500)


class PaymentCreate(PaymentBase):
    """Payment creation request."""
    pass


class PaymentResponse(PaymentBase):
    """Payment response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PaymentStatusUpdate(BaseModel):
    """Payment status update request."""
    status: str = Field(..., pattern="^(pending|authorized|failed|refunded)$")
    external_reference: Optional[str] = Field(None, max_length=255)
    failure_reason: Optional[str] = Field(None, max_length=500)


class PaymentListResponse(BaseModel):
    """Paginated payment list response."""
    items: List[PaymentResponse]
    total: int
    page: int = 1
    page_size: int = 20
