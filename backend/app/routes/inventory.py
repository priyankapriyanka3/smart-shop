"""Inventory routes for stock management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.inventory import InventoryResponse, InventoryUpdate, LowStockItem
from app.services import inventory_service

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
def list_inventory(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all inventory records (paginated, inventory_manager role)."""
    inventory_records, total = inventory_service.get_inventory_records(db, page, per_page)
    pages = (total + per_page - 1) // per_page

    return {
        "items": [InventoryResponse.model_validate(record) for record in inventory_records],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    actor_id: int = Query(..., description="Actor performing the update"),
    db: Session = Depends(get_db),
):
    """Update inventory quantity (inventory_manager role)."""
    inventory = inventory_service.update_inventory_quantity(
        db, inventory_id, inventory_update.quantity, actor_id
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return InventoryResponse.model_validate(inventory)


@router.get("/low-stock", response_model=list[LowStockItem])
def get_low_stock(db: Session = Depends(get_db)):
    """Get products at or below reorder level (inventory_manager role)."""
    low_stock_items = inventory_service.get_low_stock_items(db)
    return [LowStockItem.model_validate(item) for item in low_stock_items]
