"""Category API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryList, CategoryResponse
from app.schemas.common import PaginatedResponse
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/categories", tags=["categories"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency for product service."""
    return ProductService(db)


@router.get("", response_model=list[CategoryList])
def list_categories(
    service: ProductService = Depends(get_product_service),
):
    """
    Get all categories in hierarchical structure.

    Returns root categories with nested subcategories.
    """
    categories = service.get_category_hierarchy()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Get category details by ID."""
    category = service.get_category_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    category_dict = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "parent_id": category.parent_id,
        "is_active": category.is_active,
        "created_at": category.created_at.isoformat(),
        "updated_at": category.updated_at.isoformat(),
    }

    return CategoryResponse(**category_dict)


@router.get("/{category_id}/products", response_model=PaginatedResponse[ProductResponse])
def list_category_products(
    category_id: int,
    page: int = 1,
    per_page: int = 20,
    service: ProductService = Depends(get_product_service),
):
    """
    Get products in a specific category.

    Returns paginated list of active products.
    """
    # Verify category exists
    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    products, total = service.get_products(
        page=page,
        per_page=per_page,
        category_id=category_id,
        is_active="active",
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
