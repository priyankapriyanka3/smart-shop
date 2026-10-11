"""Promotions domain schemas: Discount campaigns."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class PromotionBase(BaseModel):
    """Base promotion schema."""
    code: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    discount_type: str = Field(
        ...,
        pattern="^(percentage|fixed|free_shipping)$"
    )
    discount_value: float = Field(..., gt=0)
    minimum_order_amount: float = Field(default=0.0, ge=0)
    start_date: datetime
    end_date: datetime
    max_uses: Optional[int] = Field(None, gt=0)
    status: str = Field(
        default="inactive",
        pattern="^(active|inactive|expired)$"
    )


class PromotionCreate(PromotionBase):
    """Promotion creation request."""
    pass


class PromotionUpdate(BaseModel):
    """Promotion update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    discount_value: Optional[float] = Field(None, gt=0)
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_uses: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(
        None,
        pattern="^(active|inactive|expired)$"
    )


class PromotionResponse(PromotionBase):
    """Promotion response."""
    id: int
    current_uses: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PromotionListResponse(BaseModel):
    """Paginated promotion list response."""
    items: List[PromotionResponse]
    total: int
    page: int
    page_size: int


class ValidatePromotionRequest(BaseModel):
    """Validate promotion eligibility request."""
    code: str = Field(..., min_length=1, max_length=100)
    order_total: float = Field(..., ge=0)


class ValidatePromotionResponse(BaseModel):
    """Promotion validation result."""
    valid: bool
    discount_amount: float = 0.0
    discount_type: str = ""
    discount_value: float = 0.0
    message: str = ""


class PromotionEligibilityResponse(BaseModel):
    """Promotion eligibility check response."""
    eligible: bool
    discount_amount: float = 0.0
    errors: List[str] = []
    promotion_name: Optional[str] = None
    discount_type: Optional[str] = None
