"""Order service for order management operations."""

from __future__ import annotations

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


def get_customer_orders(db: Session, customer_id: int, page: int = 1, per_page: int = 20) -> tuple[list[Order], int]:
    """Get paginated orders for a customer."""
    query = db.query(Order).filter(Order.customer_id == customer_id).order_by(desc(Order.created_at))
    total = query.count()
    offset = (page - 1) * per_page
    orders = query.limit(per_page).offset(offset).all()
    return orders, total


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    """Get order by ID with items."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        # Eager load items with product details
        items = (
            db.query(OrderItem)
            .join(Product)
            .filter(OrderItem.order_id == order_id)
            .all()
        )
        for item in items:
            item.product_name = item.product.name
            item.product_brand = item.product.brand
        order.items = items
    return order


def update_order_status(
    db: Session, order_id: int, new_status: str, actor_id: int
) -> Order | None:
    """Update order status and log the change."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    old_status = order.status
    order.status = new_status
    db.commit()
    db.refresh(order)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="order_status_change",
        entity_type="order",
        entity_id=order_id,
        details=f"Status changed from {old_status} to {new_status}",
    )
    db.add(audit_log)
    db.commit()

    return order


def add_order_note(db: Session, order_id: int, note: str, actor_id: int) -> bool:
    """Add a support note to an order (logged in audit trail)."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return False

    # Log the note in audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="order_note_added",
        entity_type="order",
        entity_id=order_id,
        details=note,
    )
    db.add(audit_log)
    db.commit()
    return True


def get_all_orders(db: Session, page: int = 1, per_page: int = 20) -> tuple[list[Order], int]:
    """Get all orders (admin/support view)."""
    query = db.query(Order).order_by(desc(Order.created_at))
    total = query.count()
    offset = (page - 1) * per_page
    orders = query.limit(per_page).offset(offset).all()
    return orders, total
