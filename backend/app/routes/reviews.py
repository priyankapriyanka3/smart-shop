"""Review routes for product review management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.review import ReviewCreate, ReviewHideRequest, ReviewResponse
from app.services import review_service

router = APIRouter()


@router.get("/products/{product_id}/reviews", response_model=PaginatedResponse)
def list_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    include_hidden: bool = Query(False, description="Include hidden reviews (admin only)"),
    db: Session = Depends(get_db),
):
    """Get reviews for a product (paginated)."""
    reviews, total = review_service.get_product_reviews(db, product_id, page, per_page, include_hidden)
    pages = (total + per_page - 1) // per_page

    return {
        "items": [ReviewResponse.model_validate(review) for review in reviews],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(
    review: ReviewCreate,
    customer_id: int = Query(..., description="Authenticated customer ID"),
    db: Session = Depends(get_db),
):
    """Create a new review for a product (authenticated customers only)."""
    new_review = review_service.create_review(db, customer_id, review)
    return ReviewResponse.model_validate(new_review)


@router.post("/{review_id}/helpful", response_model=ReviewResponse)
def mark_review_helpful(review_id: int, db: Session = Depends(get_db)):
    """Increment helpful count for a review."""
    review = review_service.increment_helpful_count(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewResponse.model_validate(review)


@router.patch("/{review_id}/hide", response_model=ReviewResponse)
def hide_review(
    review_id: int,
    hide_request: ReviewHideRequest,
    actor_id: int = Query(..., description="Actor performing the moderation action"),
    db: Session = Depends(get_db),
):
    """Hide or unhide a review (admin only)."""
    review = review_service.hide_review(db, review_id, hide_request.is_hidden, actor_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewResponse.model_validate(review)


@router.get("/products/{product_id}/rating")
def get_product_rating(product_id: int, db: Session = Depends(get_db)):
    """Get aggregate rating for a product."""
    rating_stats = review_service.get_aggregate_rating(db, product_id)
    return rating_stats
