"""Reviews domain service: Product reviews, aggregation, and moderation."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.reviews import Review, HelpfulVote
from app.schemas.reviews import (
    ReviewCreate,
    ReviewResponse,
    ReviewListResponse,
    ReviewAggregateResponse,
)


class ReviewService:
    """Service for review operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_review_response(self, review: Review) -> ReviewResponse:
        """Build review response with enriched data."""
        return ReviewResponse(
            id=review.id,
            product_id=review.product_id,
            customer_id=review.customer_id,
            rating=review.rating,
            title=review.title,
            review_text=review.review_text,
            status=review.status,
            helpful_count=review.helpful_count,
            customer_name=review.customer.name,
            product_name=review.product.name,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    def get_reviews(
        self,
        page: int = 1,
        page_size: int = 20,
        product_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> ReviewListResponse:
        """Get paginated list of reviews."""
        query = self.db.query(Review)

        if product_id:
            query = query.filter(Review.product_id == product_id)

        if status:
            query = query.filter(Review.status == status)

        query = query.order_by(Review.created_at.desc())

        total = query.count()
        offset = (page - 1) * page_size
        reviews = query.offset(offset).limit(page_size).all()

        return ReviewListResponse(
            items=[self.get_review_response(review) for review in reviews],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_review_by_id(self, review_id: int) -> Optional[ReviewResponse]:
        """Get review by ID."""
        review = self.db.query(Review).filter(Review.id == review_id).first()
        return self.get_review_response(review) if review else None

    def create_review(self, data: ReviewCreate) -> ReviewResponse:
        """Create a new review."""
        review = Review(
            **data.model_dump(),
            status="pending",
        )
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return self.get_review_response(review)

    def approve_review(self, review_id: int, user_id: Optional[int] = None) -> Optional[ReviewResponse]:
        """Approve a review with audit logging."""
        from app.audit.logger import log_audit
        
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return None

        review.status = "approved"
        self.db.commit()
        self.db.refresh(review)
        
        # Log audit entry for approval
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="review",
                object_id=review_id,
                action="approve",
                summary=f"Review #{review_id} approved for product '{review.product.name}'",
            )
        
        return self.get_review_response(review)

    def reject_review(self, review_id: int, user_id: Optional[int] = None) -> Optional[ReviewResponse]:
        """Reject a review with audit logging."""
        from app.audit.logger import log_audit
        
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return None

        review.status = "rejected"
        self.db.commit()
        self.db.refresh(review)
        
        # Log audit entry for rejection
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="review",
                object_id=review_id,
                action="reject",
                summary=f"Review #{review_id} rejected for product '{review.product.name}'",
            )
        
        return self.get_review_response(review)

    def add_helpful_vote(
        self,
        review_id: int,
        customer_id: int,
    ) -> bool:
        """Add helpful vote to review (idempotent)."""
        # Check if vote already exists
        existing_vote = (
            self.db.query(HelpfulVote)
            .filter(
                HelpfulVote.review_id == review_id,
                HelpfulVote.customer_id == customer_id,
            )
            .first()
        )

        if existing_vote:
            return False  # Already voted

        # Add vote
        vote = HelpfulVote(review_id=review_id, customer_id=customer_id)
        self.db.add(vote)

        # Increment helpful count
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review:
            review.helpful_count += 1

        self.db.commit()
        return True

    def get_aggregate_ratings(self, product_id: int) -> ReviewAggregateResponse:
        """Get aggregate review statistics for a product."""
        # Get approved reviews only
        reviews = (
            self.db.query(Review)
            .filter(Review.product_id == product_id, Review.status == "approved")
            .all()
        )

        if not reviews:
            return ReviewAggregateResponse(
                product_id=product_id,
                average_rating=0.0,
                total_reviews=0,
                rating_distribution={1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            )

        # Calculate average
        total_reviews = len(reviews)
        average_rating = sum(r.rating for r in reviews) / total_reviews

        # Calculate distribution
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in reviews:
            rating_distribution[review.rating] += 1

        return ReviewAggregateResponse(
            product_id=product_id,
            average_rating=round(average_rating, 2),
            total_reviews=total_reviews,
            rating_distribution=rating_distribution,
        )
