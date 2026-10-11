"""Category schemas."""

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """Base category schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class CategoryResponse(CategoryBase):
    """Category response schema."""

    id: int
    parent_id: int | None = None
    is_active: bool
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class CategoryList(BaseModel):
    """Category list with hierarchy support."""

    id: int
    name: str
    description: str | None = None
    parent_id: int | None = None
    is_active: bool
    subcategories: list["CategoryList"] = []

    model_config = ConfigDict(from_attributes=True)
