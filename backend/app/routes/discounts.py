"""Discount routes for promotion management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.discount import (
    DiscountCreate,
    DiscountResponse,
    DiscountUpdate,
    DiscountValidationRequest,
    DiscountValidationResponse,
)
from app.services import discount_service

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
def list_discounts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all discounts (paginated, admin only)."""
    discounts, total = discount_service.get_all_discounts(db, page, per_page)
    pages = (total + per_page - 1) // per_page

    return {
        "items": [DiscountResponse.model_validate(discount) for discount in discounts],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.post("/", response_model=DiscountResponse, status_code=201)
def create_discount(
    discount: DiscountCreate,
    actor_id: int = Query(..., description="Actor creating the discount"),
    db: Session = Depends(get_db),
):
    """Create a new discount (admin only)."""
    new_discount = discount_service.create_discount(db, discount, actor_id)
    return DiscountResponse.model_validate(new_discount)


@router.put("/{discount_id}", response_model=DiscountResponse)
def update_discount(
    discount_id: int,
    discount: DiscountUpdate,
    actor_id: int = Query(..., description="Actor updating the discount"),
    db: Session = Depends(get_db),
):
    """Update a discount (admin only)."""
    updated_discount = discount_service.update_discount(db, discount_id, discount, actor_id)
    if not updated_discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return DiscountResponse.model_validate(updated_discount)


@router.post("/validate", response_model=DiscountValidationResponse)
def validate_discount(validation: DiscountValidationRequest, db: Session = Depends(get_db)):
    """Validate discount code for cart total."""
    result = discount_service.validate_discount(db, validation.code, validation.cart_total)
    return DiscountValidationResponse(**result)
