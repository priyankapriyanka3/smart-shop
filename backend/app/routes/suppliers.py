"""Supplier routes for supplier management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services import supplier_service

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
def list_suppliers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all suppliers (paginated, inventory_manager role)."""
    suppliers, total = supplier_service.get_all_suppliers(db, page, per_page)
    pages = (total + per_page - 1) // per_page

    return {
        "items": [SupplierResponse.model_validate(supplier) for supplier in suppliers],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.post("/", response_model=SupplierResponse, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    actor_id: int = Query(..., description="Actor creating the supplier"),
    db: Session = Depends(get_db),
):
    """Create a new supplier (inventory_manager role)."""
    new_supplier = supplier_service.create_supplier(db, supplier, actor_id)
    return SupplierResponse.model_validate(new_supplier)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    actor_id: int = Query(..., description="Actor updating the supplier"),
    db: Session = Depends(get_db),
):
    """Update a supplier (inventory_manager role)."""
    updated_supplier = supplier_service.update_supplier(db, supplier_id, supplier, actor_id)
    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return SupplierResponse.model_validate(updated_supplier)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Get supplier details by ID (inventory_manager role)."""
    supplier = supplier_service.get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return SupplierResponse.model_validate(supplier)
