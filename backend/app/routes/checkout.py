"""Checkout routes: order creation and validation."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.customers import User
from app.services.checkout import CheckoutService
from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
    CheckoutValidationResponse,
)


router = APIRouter()


@router.post("/validate", response_model=CheckoutValidationResponse)
def validate_checkout(
    data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Validate checkout request.
    
    Checks inventory availability, promotion eligibility, and calculates totals.
    Does not create an order.
    Requires authentication.
    """
    service = CheckoutService(db)
    try:
        return service.validate_checkout(current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit", response_model=CheckoutResponse, status_code=201)
def submit_checkout(
    data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit checkout and create order.
    
    Validates inventory, applies promotions, creates order and payment records.
    Implements idempotent order creation protection.
    Requires authentication.
    """
    service = CheckoutService(db)
    try:
        return service.process_checkout(current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
