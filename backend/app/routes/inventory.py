"""Inventory routes: stock management."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models.customers import User
from app.services.inventory import InventoryService
from app.schemas.inventory import (
    InventoryResponse,
    InventoryListResponse,
    StockUpdateRequest,
    StockAdjustmentRequest,
    StockAdjustmentRequestFull,
    LowStockResponse,
)


router = APIRouter()


@router.get("/", response_model=InventoryListResponse)
def list_inventory(
    product_id: Optional[int] = Query(None),
    warehouse_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get paginated inventory records.
    
    Can filter by product_id and warehouse_id.
    Requires authentication.
    """
    service = InventoryService(db)
    return service.get_inventory(
        product_id=product_id,
        warehouse_id=warehouse_id,
        page=page,
        page_size=page_size,
    )


@router.get("/alerts/low-stock", response_model=LowStockResponse)
@router.get("/low-stock", response_model=LowStockResponse)
def get_low_stock_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get list of products with stock below reorder level."""
    service = InventoryService(db)
    return service.get_low_stock_items(page=page, page_size=page_size)


@router.get("/product/{product_id}/availability", response_model=InventoryResponse)
def get_product_availability(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Get total available stock for a product across all warehouses."""
    service = InventoryService(db)
    return service.get_product_total_stock(product_id)


@router.post("/adjust", response_model=InventoryResponse)
def adjust_stock(
    data: StockAdjustmentRequestFull,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Adjust inventory stock level with audit logging (legacy format).
    
    Records adjustment with reason and user for audit trail.
    """
    service = InventoryService(db)
    try:
        return service.adjust_stock(
            inventory_id=data.inventory_id,
            quantity_change=data.quantity_change,
            reason=data.reason,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db),
):
    """Get inventory record by ID."""
    service = InventoryService(db)
    inventory = service.get_inventory_by_id(inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inventory


@router.patch("/{inventory_id}", response_model=InventoryResponse)
def update_stock_quantity(
    inventory_id: int,
    data: StockUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """
    Update inventory stock quantity (set to specific value).
    
    Records change with reason and user for audit trail.
    Requires admin role.
    """
    service = InventoryService(db)
    try:
        inventory = service.get_inventory_by_id(inventory_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory record not found")
        
        quantity_change = data.quantity - inventory.quantity
        return service.adjust_stock(
            inventory_id=inventory_id,
            quantity_change=quantity_change,
            reason=data.reason,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{inventory_id}/adjust", response_model=InventoryResponse)
def adjust_stock_relative(
    inventory_id: int,
    data: StockAdjustmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """
    Adjust inventory stock by relative amount (+/-).
    
    Records adjustment with reason and user for audit trail.
    Requires admin role.
    """
    service = InventoryService(db)
    try:
        return service.adjust_stock(
            inventory_id=inventory_id,
            quantity_change=data.adjustment,
            reason=data.reason,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
