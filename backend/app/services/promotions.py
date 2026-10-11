"""Promotions domain service: Discount campaign management and eligibility validation."""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.promotions import Promotion
from app.schemas.promotions import (
    PromotionCreate,
    PromotionUpdate,
    PromotionResponse,
    PromotionListResponse,
    PromotionEligibilityResponse,
)


class PromotionService:
    """Service for promotion operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_promotions(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> PromotionListResponse:
        """Get paginated list of promotions."""
        query = self.db.query(Promotion)

        if status:
            query = query.filter(Promotion.status == status)

        query = query.order_by(Promotion.created_at.desc())

        total = query.count()
        offset = (page - 1) * page_size
        promotions = query.offset(offset).limit(page_size).all()

        return PromotionListResponse(
            items=[PromotionResponse.model_validate(promo) for promo in promotions],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_promotion_by_id(self, promotion_id: int) -> Optional[PromotionResponse]:
        """Get promotion by ID."""
        promotion = self.db.query(Promotion).filter(Promotion.id == promotion_id).first()
        return PromotionResponse.model_validate(promotion) if promotion else None

    def get_promotion_by_code(self, code: str) -> Optional[Promotion]:
        """Get promotion by code (returns ORM model)."""
        return self.db.query(Promotion).filter(Promotion.code == code).first()

    def create_promotion(self, data: PromotionCreate) -> PromotionResponse:
        """Create a new promotion."""
        promotion = Promotion(**data.model_dump())
        self.db.add(promotion)
        self.db.commit()
        self.db.refresh(promotion)
        return PromotionResponse.model_validate(promotion)

    def update_promotion(
        self,
        promotion_id: int,
        data: PromotionUpdate,
    ) -> Optional[PromotionResponse]:
        """Update promotion."""
        promotion = self.db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(promotion, key, value)

        self.db.commit()
        self.db.refresh(promotion)
        return PromotionResponse.model_validate(promotion)

    def check_eligibility(
        self,
        code: str,
        order_amount: float,
    ) -> PromotionEligibilityResponse:
        """Check promotion eligibility and calculate discount."""
        promotion = self.get_promotion_by_code(code)

        if not promotion:
            return PromotionEligibilityResponse(
                eligible=False,
                errors=["Promotion code not found"],
            )

        errors = []

        # Check if promotion is active
        if promotion.status != "active":
            errors.append("Promotion is not active")

        # Check date range
        now = datetime.utcnow()
        if now < promotion.start_date:
            errors.append("Promotion has not started yet")
        if now > promotion.end_date:
            errors.append("Promotion has expired")

        # Check minimum order amount
        if order_amount < promotion.minimum_order_amount:
            errors.append(
                f"Minimum order amount of ${promotion.minimum_order_amount:.2f} not met"
            )

        # Check usage limit
        if promotion.max_uses is not None:
            if promotion.current_uses >= promotion.max_uses:
                errors.append("Promotion usage limit reached")

        if errors:
            return PromotionEligibilityResponse(
                eligible=False,
                errors=errors,
            )

        # Calculate discount
        discount_amount = 0.0
        if promotion.discount_type == "percentage":
            discount_amount = order_amount * (promotion.discount_value / 100.0)
        elif promotion.discount_type == "fixed":
            discount_amount = min(promotion.discount_value, order_amount)
        elif promotion.discount_type == "free_shipping":
            # Free shipping promotions don't reduce order amount directly
            # The shipping cost is handled separately in checkout
            discount_amount = 0.0

        return PromotionEligibilityResponse(
            eligible=True,
            discount_amount=discount_amount,
            promotion_name=promotion.name,
            discount_type=promotion.discount_type,
        )

    def increment_usage(self, code: str) -> bool:
        """Increment promotion usage count."""
        promotion = self.get_promotion_by_code(code)
        if not promotion:
            return False

        promotion.current_uses += 1
        self.db.commit()
        return True

    def activate_promotion(self, promotion_id: int, user_id: Optional[int] = None) -> Optional[PromotionResponse]:
        """Activate a promotion with audit logging."""
        from app.audit.logger import log_audit
        
        promotion = self.db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return None

        promotion.status = "active"
        self.db.commit()
        self.db.refresh(promotion)
        
        # Log audit entry for activation
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="promotion",
                object_id=promotion_id,
                action="activate",
                summary=f"Promotion '{promotion.code}' activated",
            )
        
        return PromotionResponse.model_validate(promotion)

    def deactivate_promotion(self, promotion_id: int, user_id: Optional[int] = None) -> Optional[PromotionResponse]:
        """Deactivate a promotion with audit logging."""
        from app.audit.logger import log_audit
        
        promotion = self.db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return None

        promotion.status = "inactive"
        self.db.commit()
        self.db.refresh(promotion)
        
        # Log audit entry for deactivation
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="promotion",
                object_id=promotion_id,
                action="deactivate",
                summary=f"Promotion '{promotion.code}' deactivated",
            )
        
        return PromotionResponse.model_validate(promotion)
