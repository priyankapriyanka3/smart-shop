"""Supplier service for supplier management operations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def get_all_suppliers(db: Session, page: int = 1, per_page: int = 20) -> tuple[list[Supplier], int]:
    """Get paginated suppliers."""
    query = db.query(Supplier).order_by(Supplier.name)
    total = query.count()
    offset = (page - 1) * per_page
    suppliers = query.limit(per_page).offset(offset).all()
    return suppliers, total


def get_supplier_by_id(db: Session, supplier_id: int) -> Supplier | None:
    """Get supplier by ID."""
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def create_supplier(db: Session, supplier_data: SupplierCreate, actor_id: int) -> Supplier:
    """Create a new supplier."""
    supplier = Supplier(
        name=supplier_data.name,
        contact_name=supplier_data.contact_name,
        email=supplier_data.email,
        phone=supplier_data.phone,
        country=supplier_data.country,
        website=supplier_data.website,
        lead_time_days=supplier_data.lead_time_days,
        rating=supplier_data.rating,
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="supplier_create",
        entity_type="supplier",
        entity_id=supplier.id,
        details=f"Created supplier: {supplier.name}",
    )
    db.add(audit_log)
    db.commit()

    return supplier


def update_supplier(
    db: Session, supplier_id: int, supplier_data: SupplierUpdate, actor_id: int
) -> Supplier | None:
    """Update an existing supplier."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        return None

    update_fields = supplier_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(supplier, field, value)

    db.commit()
    db.refresh(supplier)

    # Log audit trail
    audit_log = AuditLog(
        actor_id=actor_id,
        action="supplier_update",
        entity_type="supplier",
        entity_id=supplier_id,
        details=f"Updated supplier: {supplier.name}",
    )
    db.add(audit_log)
    db.commit()

    return supplier
