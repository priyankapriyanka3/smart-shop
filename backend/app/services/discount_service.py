"""Discount service for promotion management operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate


def get_all_discounts(db: Session, page: int = 1, per_page: int = 20) -> tuple[list[Discount], int]:
    """Get paginated discounts (admin view)."""
    query = db.query(Discount).order_by(Discount.created_at.desc())
    total = query.count()
    offset = (page - 1) * per_page
    discounts = query.limit(per_page).offset(offset).all()
    return discounts, total


def get_discount_by_id(db: Session, discount_id: int) -> Discount | None:
    """Get discount by ID."""
    return db.query(Discount).filter(Discount.id == discount_id).first()


def create_discount(db: Session, discount_data: DiscountCreate, actor_id: int) -> Discount:
    """Create a new discount."""
    discount = Discount(
        code=discount_data.code,
        discount_type=discount_data.discount_type,
        discount_value=discount_data.discount_value,
        min_order_amount=discount_data.min_order_amount,
        valid_from=discount_data.valid_from,
        valid_to=discount_data.valid_to,
        max_uses=discount_data.max_uses,
        is_active=discount_data.is_active,
        times_used=0,
    )
    db.add(discount)
    db.commit()
    db.refresh(discount)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="discount_create",
        entity_type="discount",
        entity_id=discount.id,
        details=f"Created discount code: {discount.code}",
    )
    db.add(audit_log)
    db.commit()

    return discount


def update_discount(
    db: Session, discount_id: int, discount_data: DiscountUpdate, actor_id: int
) -> Discount | None:
    """Update an existing discount."""
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        return None

    update_fields = discount_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(discount, field, value)

    db.commit()
    db.refresh(discount)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="discount_update",
        entity_type="discount",
        entity_id=discount_id,
        details=f"Updated discount code: {discount.code}",
    )
    db.add(audit_log)
    db.commit()

    return discount


def validate_discount(db: Session, code: str, cart_total: Decimal) -> dict:
    """Validate discount code for cart total."""
    discount = db.query(Discount).filter(Discount.code == code).first()

    if not discount:
        return {"valid": False, "error": "Discount code not found"}

    if not discount.is_active:
        return {"valid": False, "error": "Discount code is inactive"}

    now = datetime.utcnow()
    if now < discount.valid_from:
        return {"valid": False, "error": "Discount code is not yet valid"}

    if now > discount.valid_to:
        return {"valid": False, "error": "Discount code has expired"}

    if discount.max_uses is not None and discount.times_used >= discount.max_uses:
        return {"valid": False, "error": "Discount code usage limit reached"}

    if discount.min_order_amount is not None and cart_total < discount.min_order_amount:
        return {
            "valid": False,
            "error": f"Minimum order amount is {discount.min_order_amount}",
        }

    return {
        "valid": True,
        "discount_id": discount.id,
        "discount_value": discount.discount_value,
        "discount_type": discount.discount_type,
    }


def increment_discount_usage(db: Session, discount_id: int) -> bool:
    """Atomically increment discount usage count."""
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        return False

    # Check max_uses before incrementing
    if discount.max_uses is not None and discount.times_used >= discount.max_uses:
        return False

    discount.times_used += 1
    db.commit()
    return True
