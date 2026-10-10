"""Common Pydantic schemas."""
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""

    items: List[T]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    pages: int = Field(..., description="Total number of pages")

    @staticmethod
    def create(items: List[T], total: int, page: int, per_page: int) -> "PaginatedResponse[T]":
        """Create paginated response."""
        pages = (total + per_page - 1) // per_page if total > 0 else 0
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )
