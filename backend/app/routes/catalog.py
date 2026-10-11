"""Catalog routes: products, categories, search."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.catalog import CatalogService
from app.schemas.catalog import (
    CategoryResponse,
    CategoryListResponse,
    ProductResponse,
    ProductListResponse,
)


router = APIRouter()


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get paginated list of categories."""
    service = CatalogService(db)
    return service.get_categories(page=page, page_size=page_size, status=status)


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """Get category by ID."""
    service = CatalogService(db)
    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/categories/slug/{slug}", response_model=CategoryResponse)
def get_category_by_slug(
    slug: str,
    db: Session = Depends(get_db),
):
    """Get category by slug."""
    service = CatalogService(db)
    category = service.get_category_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/products", response_model=ProductListResponse)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    brand: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    query: Optional[str] = Query(""),
    db: Session = Depends(get_db),
):
    """Get paginated list of products with search and filters."""
    service = CatalogService(db)
    return service.search_products(
        query=query,
        page=page,
        page_size=page_size,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        sort_by=sort_by
    )


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Get product by ID with availability."""
    service = CatalogService(db)
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/search", response_model=ProductListResponse)
def search_products(
    q: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    brand: Optional[str] = Query(None),
    sort_by: str = Query("relevance", pattern="^(relevance|price_asc|price_desc|newest|rating)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Search and filter products.
    
    Supports keyword search, category filter, price range, brand filter, and sorting.
    """
    service = CatalogService(db)
    return service.search_products(
        query=q or "",
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        sort_by=sort_by,
        page=page,
        page_size=page_size,
    )
