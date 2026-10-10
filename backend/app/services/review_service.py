"""Review service for product review operations."""

from __future__ import annotations

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.customer import Customer
from app.models.review import Review
from app.schemas.review import ReviewCreate


def get_product_reviews(
    db: Session, product_id: int, page: int = 1, per_page: int = 20, include_hidden: bool = False
) -> tuple[list[Review], int]:
    """Get paginated reviews for a product."""
    query = db.query(Review).filter(Review.product_id == product_id)

    if not include_hidden:
        query = query.filter(Review.is_hidden.is_(False))

    query = query.order_by(desc(Review.created_at))
    total = query.count()
    offset = (page - 1) * per_page
    reviews = query.limit(per_page).offset(offset).all()

    # Enrich with customer names
    for review in reviews:
        customer = db.query(Customer).filter(Customer.id == review.customer_id).first()
        review.customer_name = customer.full_name if customer else "Anonymous"

    return reviews, total


def create_review(db: Session, customer_id: int, review_data: ReviewCreate) -> Review:
    """Create a new review for a product."""
    review = Review(
        product_id=review_data.product_id,
        customer_id=customer_id,
        rating=review_data.rating,
        review_text=review_data.review_text,
        helpful_count=0,
        is_hidden=False,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    # Enrich with customer name
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    review.customer_name = customer.full_name if customer else "Anonymous"

    return review


def increment_helpful_count(db: Session, review_id: int) -> Review | None:
    """Increment helpful count for a review."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None

    review.helpful_count += 1
    db.commit()
    db.refresh(review)

    # Enrich with customer name
    customer = db.query(Customer).filter(Customer.id == review.customer_id).first()
    review.customer_name = customer.full_name if customer else "Anonymous"

    return review


def hide_review(db: Session, review_id: int, is_hidden: bool, actor_id: int) -> Review | None:
    """Hide or unhide a review (moderation action)."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None

    review.is_hidden = is_hidden
    db.commit()
    db.refresh(review)

    # Log audit trail
    action_text = "hidden" if is_hidden else "unhidden"
    audit_log = AuditLog(
        actor_id=actor_id,
        action="review_hide",
        entity_type="review",
        entity_id=review_id,
        details=f"Review {action_text} for product {review.product_id}",
    )
    db.add(audit_log)
    db.commit()

    # Enrich with customer name
    customer = db.query(Customer).filter(Customer.id == review.customer_id).first()
    review.customer_name = customer.full_name if customer else "Anonymous"

    return review


def get_aggregate_rating(db: Session, product_id: int) -> dict:
    """Get aggregate rating stats for a product."""
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id, Review.is_hidden.is_(False))
        .all()
    )

    if not reviews:
        return {"average_rating": 0.0, "review_count": 0}

    total_rating = sum(r.rating for r in reviews)
    average_rating = total_rating / len(reviews)

    return {"average_rating": round(average_rating, 1), "review_count": len(reviews)}
