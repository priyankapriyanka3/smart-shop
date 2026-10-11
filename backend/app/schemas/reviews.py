"""Reviews domain schemas: Product reviews and moderation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ReviewBase(BaseModel):
    """Base review schema."""
    product_id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Review creation request."""
    pass


class ReviewResponse(ReviewBase):
    """Review response with customer details."""
    id: int
    status: str
    helpful_count: int
    customer_name: str
    product_name: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ReviewListResponse(BaseModel):
    """Paginated review list response."""
    items: List[ReviewResponse]
    total: int
    page: int
    page_size: int


class ReviewModerationRequest(BaseModel):
    """Review moderation request."""
    status: str = Field(..., pattern="^(approved|rejected)$")


class ReviewAggregateResponse(BaseModel):
    """Review aggregate statistics for a product."""
    product_id: int
    average_rating: float
    total_reviews: int
    rating_distribution: dict[int, int]  # rating -> count
