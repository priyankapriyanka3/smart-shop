"""Review routes: product reviews and moderation."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.reviews import ReviewService
from app.schemas.reviews import (
    ReviewCreate,
    ReviewResponse,
    ReviewListResponse,
)


router = APIRouter()


@router.get("/", response_model=ReviewListResponse)
def list_reviews(
    product_id: Optional[int] = Query(None),
    customer_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of reviews.
    
    Can filter by product_id, customer_id, and status.
    """
    service = ReviewService(db)
    return service.get_reviews(
        product_id=product_id,
        status=status,
        page=page,
        page_size=page_size,
    )


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    """Get review by ID."""
    service = ReviewService(db)
    review = service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
):
    """
    Submit a product review.
    
    Creates review with pending status for moderation.
    """
    service = ReviewService(db)
    try:
        return service.create_review(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/product/{product_id}/summary")
def get_product_review_summary(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Get review summary for a product.
    
    Returns average rating, total count, and rating distribution.
    """
    service = ReviewService(db)
    return service.get_aggregate_ratings(product_id)
