"""Admin routes: operational management."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models.customers import User
from app.services.admin import AdminService


router = APIRouter()


@router.get("/dashboard")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """
    Get admin dashboard statistics.
    
    Returns key metrics for inventory, orders, customers, and revenue.
    """
    service = AdminService(db)
    return service.get_dashboard_stats()


@router.post("/reviews/{review_id}/approve")
def approve_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve a pending review with audit logging."""
    service = AdminService(db)
    try:
        return service.approve_review(review_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/reviews/{review_id}/reject")
def reject_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reject a pending review with audit logging."""
    service = AdminService(db)
    try:
        return service.reject_review(review_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update order status with audit logging."""
    service = AdminService(db)
    try:
        return service.update_order_status(order_id, status, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/promotions/{promotion_id}/activate")
def activate_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Activate a promotion with audit logging."""
    service = AdminService(db)
    try:
        return service.activate_promotion(promotion_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/promotions/{promotion_id}/deactivate")
def deactivate_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deactivate a promotion with audit logging."""
    service = AdminService(db)
    try:
        return service.deactivate_promotion(promotion_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
