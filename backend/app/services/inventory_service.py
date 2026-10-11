"""Inventory service for stock management operations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse


def get_inventory_records(db: Session, page: int = 1, per_page: int = 20) -> tuple[list[Inventory], int]:
    """Get paginated inventory records with product and warehouse details."""
    query = (
        db.query(Inventory)
        .join(Product)
        .join(Warehouse)
        .order_by(Inventory.last_updated.desc())
    )
    total = query.count()
    offset = (page - 1) * per_page
    inventory_records = query.limit(per_page).offset(offset).all()

    # Enrich with product and warehouse names
    for record in inventory_records:
        record.product_name = record.product.name
        record.product_sku = record.product.sku
        record.warehouse_name = record.warehouse.name

    return inventory_records, total


def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory | None:
    """Get inventory record by ID."""
    inventory = (
        db.query(Inventory)
        .join(Product)
        .join(Warehouse)
        .filter(Inventory.id == inventory_id)
        .first()
    )
    if inventory:
        inventory.product_name = inventory.product.name
        inventory.product_sku = inventory.product.sku
        inventory.warehouse_name = inventory.warehouse.name
    return inventory


def update_inventory_quantity(
    db: Session, inventory_id: int, new_quantity: int, actor_id: int
) -> Inventory | None:
    """Update inventory quantity and log the change."""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        return None

    old_quantity = inventory.quantity
    inventory.quantity = new_quantity
    from datetime import datetime
    inventory.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(inventory)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="inventory_update",
        entity_type="inventory",
        entity_id=inventory_id,
        details=f"Quantity changed from {old_quantity} to {new_quantity}",
    )
    db.add(audit_log)
    db.commit()

    # Enrich response
    inventory.product_name = inventory.product.name
    inventory.product_sku = inventory.product.sku
    inventory.warehouse_name = inventory.warehouse.name

    return inventory


def get_low_stock_items(db: Session) -> list[dict]:
    """Get products at or below reorder level with supplier context."""
    low_stock = (
        db.query(Inventory, Product, Warehouse)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .filter(Inventory.quantity <= Inventory.reorder_level)
        .all()
    )

    results = []
    for inv, product, warehouse in low_stock:
        results.append({
            "id": inv.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_quantity": inv.quantity,
            "reorder_level": inv.reorder_level,
            "supplier_name": None,  # Will be available after supplier association
            "supplier_lead_time_days": None,
        })

    return results
