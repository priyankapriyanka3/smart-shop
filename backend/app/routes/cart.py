"""Cart routes: cart management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.customers import User
from app.services.cart import CartService
from app.schemas.cart import (
    CartResponse,
    AddToCartRequest,
    UpdateCartItemRequest,
)


router = APIRouter()


@router.get("/", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get current user's active cart with items.
    
    Creates a new cart if none exists.
    Requires authentication.
    """
    service = CartService(db)
    return service.get_or_create_cart(current_user.id)


@router.get("/{customer_id}", response_model=CartResponse)
def get_cart_by_id(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Get customer's active cart with items by customer ID.
    
    Creates a new cart if none exists.
    """
    service = CartService(db)
    return service.get_or_create_cart(customer_id)


@router.post("/items", response_model=CartResponse)
def add_to_cart(
    data: AddToCartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add item to cart.
    
    Validates stock availability before adding.
    Requires authentication.
    """
    from app.schemas.cart import CartItemCreate
    service = CartService(db)
    try:
        # Use authenticated user's ID instead of customer_id from request
        item_data = CartItemCreate(product_id=data.product_id, quantity=data.quantity)
        return service.add_item(current_user.id, item_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/items/{cart_item_id}", response_model=CartResponse)
def update_cart_item(
    cart_item_id: int,
    data: UpdateCartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update cart item quantity.
    
    Validates stock availability before updating.
    Requires authentication.
    """
    from app.schemas.cart import CartItemUpdate
    service = CartService(db)
    try:
        item_data = CartItemUpdate(quantity=data.quantity)
        return service.update_item(current_user.id, cart_item_id, item_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/items/{cart_item_id}", response_model=CartResponse)
def remove_cart_item(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remove item from cart.
    
    Requires authentication.
    """
    service = CartService(db)
    try:
        return service.remove_item(current_user.id, cart_item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/clear", response_model=CartResponse)
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Clear all items from current user's cart.
    
    Requires authentication.
    """
    service = CartService(db)
    return service.clear_cart(current_user.id)
