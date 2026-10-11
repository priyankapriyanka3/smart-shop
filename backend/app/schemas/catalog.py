"""Catalog domain schemas: Categories and Products."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    status: str = Field(default="active", pattern="^(active|inactive)$")


class CategoryCreate(CategoryBase):
    """Category creation request."""
    pass


class CategoryResponse(CategoryBase):
    """Category response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    """Paginated category list response."""
    items: List[CategoryResponse]
    total: int
    page: int
    page_size: int


class ProductBase(BaseModel):
    """Base product schema."""
    category_id: int = Field(..., gt=0)
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=500)
    slug: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = Field(None, max_length=1000)
    status: str = Field(default="active", pattern="^(active|inactive|discontinued)$")


class ProductCreate(ProductBase):
    """Product creation request."""
    pass


class ProductResponse(ProductBase):
    """Product response with availability."""
    id: int
    created_at: datetime
    updated_at: datetime
    available_quantity: Optional[int] = None  # Calculated from inventory
    
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Paginated product list response."""
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int


class ProductSearchRequest(BaseModel):
    """Product search request."""
    query: Optional[str] = Field(None, min_length=3, max_length=255)
    category_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    brand: Optional[str] = Field(None, max_length=255)
    sort_by: str = Field(default="relevance", pattern="^(relevance|price_asc|price_desc|newest|rating)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
