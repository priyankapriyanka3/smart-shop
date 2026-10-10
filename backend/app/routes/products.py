"""Product API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency for product service."""
    return ProductService(db)


@router.get("", response_model=PaginatedResponse[ProductResponse])
def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    category_id: int | None = Query(None, description="Filter by category"),
    is_active: str | None = Query(None, description="Filter by active status"),
    service: ProductService = Depends(get_product_service),
):
    """
    List products with pagination.

    Only returns active products for non-admin users.
    """
    products, total = service.get_products(
        page=page,
        per_page=per_page,
        category_id=category_id,
        is_active=is_active or "active",  # Default to active for shoppers
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


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Get product details by ID."""
    product = service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

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

    return ProductResponse(**product_dict)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """
    Create new product (admin only).

    Product starts in draft state and must be activated separately.
    """
    try:
        product = service.create_product(product_data)
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

        return ProductResponse(**product_dict)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Update product (admin only)."""
    product = service.update_product(product_id, product_data)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

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

    return ProductResponse(**product_dict)


@router.patch("/{product_id}/activate", response_model=ProductResponse)
def activate_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Activate product (admin only)."""
    try:
        product = service.activate_product(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

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

        return ProductResponse(**product_dict)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.patch("/{product_id}/deactivate", response_model=ProductResponse)
def deactivate_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Deactivate product (admin only)."""
    product = service.deactivate_product(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

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

    return ProductResponse(**product_dict)
