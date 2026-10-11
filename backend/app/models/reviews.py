"""Reviews domain models: Product reviews and helpful votes."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Review(Base):
    """Product review by a customer."""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(255), nullable=True)
    review_text = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="pending")  # pending, approved, rejected
    helpful_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
    customer = relationship("User", back_populates="reviews")
    helpful_votes = relationship("HelpfulVote", back_populates="review", cascade="all, delete-orphan")


class HelpfulVote(Base):
    """Helpful vote on a review (anti-abuse: one vote per customer per review)."""
    __tablename__ = "helpful_votes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    review = relationship("Review", back_populates="helpful_votes")


# Indexes for performance
Index("idx_review_product", Review.product_id)
Index("idx_review_customer", Review.customer_id)
Index("idx_review_status", Review.status)
Index("idx_helpful_vote_review", HelpfulVote.review_id)
Index("idx_helpful_vote_customer", HelpfulVote.customer_id)
# Unique constraint to prevent duplicate helpful votes
Index("idx_helpful_vote_unique", HelpfulVote.review_id, HelpfulVote.customer_id, unique=True)
