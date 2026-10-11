"""Review schemas for request/response models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    """Review creation request."""
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    review_text: str | None = Field(None, max_length=2000)


class ReviewResponse(BaseModel):
    """Review response model."""
    id: int
    product_id: int
    customer_id: int
    rating: int
    review_text: str | None = None
    helpful_count: int
    is_hidden: bool
    created_at: datetime
    updated_at: datetime
    customer_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ReviewHideRequest(BaseModel):
    """Review hide/unhide request."""
    is_hidden: bool = Field(..., description="True to hide, False to show")
