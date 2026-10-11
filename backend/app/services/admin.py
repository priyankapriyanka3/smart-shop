"""Admin domain service: Dashboard statistics and operations."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.orders import Order
from app.models.inventory import Inventory
from app.models.reviews import Review
from app.models.promotions import Promotion
from app.schemas.admin import StatsResponse, DashboardResponse


class AdminService:
    """Service for admin operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_stats(self) -> DashboardResponse:
        """Get admin dashboard statistics."""
        # Total orders
        total_orders = self.db.query(func.count(Order.id)).scalar() or 0

        # Total revenue
        total_revenue = self.db.query(func.sum(Order.total)).scalar() or 0.0

        # Low stock count
        low_stock_count = (
            self.db.query(func.count(Inventory.id))
            .filter(Inventory.status.in_(["low_stock", "out_of_stock"]))
            .scalar()
            or 0
        )

        # Pending orders count
        pending_orders_count = (
            self.db.query(func.count(Order.id))
            .filter(Order.status.in_(["placed", "processing"]))
            .scalar()
            or 0
        )

        # Pending reviews count
        pending_reviews_count = (
            self.db.query(func.count(Review.id))
            .filter(Review.status == "pending")
            .scalar()
            or 0
        )

        # Build stats cards
        stats = [
            StatsResponse(
                label="Total Orders",
                value=total_orders,
                trend="neutral",
            ),
            StatsResponse(
                label="Total Revenue",
                value=f"${total_revenue:,.2f}",
                trend="positive" if total_revenue > 0 else "neutral",
            ),
            StatsResponse(
                label="Low Stock Items",
                value=low_stock_count,
                trend="negative" if low_stock_count > 0 else "positive",
            ),
            StatsResponse(
                label="Pending Orders",
                value=pending_orders_count,
                trend="neutral",
            ),
        ]

        return DashboardResponse(
            stats=stats,
            low_stock_count=low_stock_count,
            pending_orders_count=pending_orders_count,
            pending_reviews_count=pending_reviews_count,
        )

    def approve_review(self, review_id: int, user_id: Optional[int] = None):
        """Approve a review with audit logging."""
        from app.services.reviews import ReviewService
        
        service = ReviewService(self.db)
        result = service.approve_review(review_id, user_id=user_id)
        if not result:
            raise ValueError(f"Review {review_id} not found")
        return result

    def reject_review(self, review_id: int, user_id: Optional[int] = None):
        """Reject a review with audit logging."""
        from app.services.reviews import ReviewService
        
        service = ReviewService(self.db)
        result = service.reject_review(review_id, user_id=user_id)
        if not result:
            raise ValueError(f"Review {review_id} not found")
        return result

    def update_order_status(self, order_id: int, status: str, user_id: Optional[int] = None):
        """Update order status with audit logging."""
        from app.services.orders import OrderService
        
        valid_statuses = ["placed", "processing", "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}")
        
        service = OrderService(self.db)
        result = service.update_order_status(order_id, status, user_id=user_id)
        if not result:
            raise ValueError(f"Order {order_id} not found")
        return result

    def activate_promotion(self, promotion_id: int, user_id: Optional[int] = None):
        """Activate a promotion with audit logging."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(self.db)
        result = service.activate_promotion(promotion_id, user_id=user_id)
        if not result:
            raise ValueError(f"Promotion {promotion_id} not found")
        return result

    def deactivate_promotion(self, promotion_id: int, user_id: Optional[int] = None):
        """Deactivate a promotion with audit logging."""
        from app.services.promotions import PromotionService
        
        service = PromotionService(self.db)
        result = service.deactivate_promotion(promotion_id, user_id=user_id)
        if not result:
            raise ValueError(f"Promotion {promotion_id} not found")
        return result
