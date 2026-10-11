"""Promotion routes: discount campaign management."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import require_role
from app.models.customers import User
from app.services.promotions import PromotionService
from app.schemas.promotions import (
    PromotionCreate,
    PromotionResponse,
    PromotionListResponse,
    ValidatePromotionRequest,
    ValidatePromotionResponse,
)


router = APIRouter()


@router.get("/", response_model=PromotionListResponse)
def list_promotions(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of promotions.
    
    Can filter by status (active, expired, exhausted).
    """
    service = PromotionService(db)
    return service.get_promotions(status=status, page=page, page_size=page_size)


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
):
    """Get promotion by ID."""
    service = PromotionService(db)
    promotion = service.get_promotion_by_id(promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


@router.get("/code/{code}", response_model=PromotionResponse)
def get_promotion_by_code(
    code: str,
    db: Session = Depends(get_db),
):
    """Get promotion by code."""
    service = PromotionService(db)
    promotion = service.get_promotion_by_code(code)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


@router.post("/validate", response_model=ValidatePromotionResponse)
def validate_promotion(
    data: ValidatePromotionRequest,
    db: Session = Depends(get_db),
):
    """
    Validate promotion eligibility.
    
    Checks active status, date range, minimum order threshold, and usage limit.
    """
    service = PromotionService(db)
    try:
        return service.check_eligibility(data.code, data.order_total)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=PromotionResponse, status_code=201, dependencies=[Depends(require_role("admin"))])
def create_promotion(
    data: PromotionCreate,
    db: Session = Depends(get_db),
):
    """Create a new promotion. Requires admin role."""
    service = PromotionService(db)
    return service.create_promotion(data)


@router.post("/{promotion_id}/activate", response_model=PromotionResponse)
def activate_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
):
    """Activate a promotion."""
    from app.schemas.promotions import PromotionUpdate
    service = PromotionService(db)
    result = service.update_promotion(promotion_id, PromotionUpdate(status="active"))
    if not result:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return result


@router.post("/{promotion_id}/deactivate", response_model=PromotionResponse)
def deactivate_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
):
    """Deactivate a promotion."""
    from app.schemas.promotions import PromotionUpdate
    service = PromotionService(db)
    result = service.update_promotion(promotion_id, PromotionUpdate(status="inactive"))
    if not result:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return result
