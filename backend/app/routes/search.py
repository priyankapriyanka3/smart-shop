"""Search and discovery API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/search", tags=["search"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency for product service."""
    return ProductService(db)


@router.get("", response_model=PaginatedResponse[ProductResponse])
def search_products(
    q: str | None = Query(None, description="Search query"),
    category_id: int | None = Query(None, description="Filter by category"),
    min_price: float | None = Query(None, ge=0, description="Minimum price"),
    max_price: float | None = Query(None, ge=0, description="Maximum price"),
    brand: str | None = Query(None, description="Filter by brand"),
    min_rating: float | None = Query(None, ge=1, le=5, description="Minimum rating"),
    in_stock: bool | None = Query(None, description="Filter in-stock products only"),
    sort: str = Query("relevance", description="Sort by: relevance, price_asc, price_desc, rating, newest"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    service: ProductService = Depends(get_product_service),
):
    """
    Search products with filters and sorting.

    Supports keyword search across name, brand, and description.
    Filters: category, price range, brand, rating, availability.
    Sort options: relevance, price_asc, price_desc, rating, newest.
    """
    products, total = service.search_products(
        query=q,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        min_rating=min_rating,
        in_stock=in_stock,
        sort_by=sort,
        page=page,
        per_page=per_page,
    )

    # Convert to response models with stock status
    product_responses = []
    for product in products:
        stock_status = service._compute_stock_status(product)
        product_dict = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "brand": product.brand,
            "sku": product.sku,
            "price": product.price,
            "category_id": product.category_id,
            "is_active": product.is_active,
            "stock_status": stock_status,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }
        product_responses.append(ProductResponse(**product_dict))

    return PaginatedResponse.create(
        items=product_responses,
        total=total,
        page=page,
        per_page=per_page,
    )
