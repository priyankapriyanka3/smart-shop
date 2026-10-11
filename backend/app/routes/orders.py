"""Order routes: order history and status tracking."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.customers import User
from app.services.orders import OrderService
from app.schemas.orders import (
    OrderResponse,
    OrderListResponse,
    OrderDetailResponse,
)


router = APIRouter()


@router.get("/", response_model=OrderListResponse)
def list_orders(
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of orders for the current user.
    
    Can filter by status.
    Requires authentication.
    """
    service = OrderService(db)
    return service.get_orders(
        customer_id=current_user.id,
        status=status,
        page=page,
        page_size=page_size,
    )


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get order detail by ID with items and payment info.
    
    Requires authentication. Users can only view their own orders.
    """
    service = OrderService(db)
    order = service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify the order belongs to the current user
    if order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order


@router.get("/customer/{customer_id}/history", response_model=OrderListResponse)
def get_customer_orders(
    customer_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get order history for a customer (admin endpoint)."""
    service = OrderService(db)
    return service.get_orders(customer_id=customer_id, page=page, page_size=page_size)
