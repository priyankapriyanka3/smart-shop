"""Order routes for order management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.order import OrderNoteCreate, OrderResponse, OrderStatusUpdate
from app.services import order_service

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
def list_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    customer_id: int = Query(..., description="Customer ID filter"),
    db: Session = Depends(get_db),
):
    """List orders for a customer (paginated)."""
    orders, total = order_service.get_customer_orders(db, customer_id, page, per_page)
    pages = (total + per_page - 1) // per_page

    return {
        "items": [OrderResponse.model_validate(order) for order in orders],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order details by ID."""
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    actor_id: int = Query(..., description="Actor performing the update"),
    db: Session = Depends(get_db),
):
    """Update order status (admin only)."""
    order = order_service.update_order_status(db, order_id, status_update.status, actor_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)


@router.post("/{order_id}/notes", status_code=201)
def add_order_note(
    order_id: int,
    note: OrderNoteCreate,
    actor_id: int = Query(..., description="Actor adding the note"),
    db: Session = Depends(get_db),
):
    """Add a support note to an order (support role only)."""
    success = order_service.add_order_note(db, order_id, note.note, actor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Note added successfully"}
