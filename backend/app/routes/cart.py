"""Cart API routes."""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
    ProductSummary,
)
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    """Dependency for cart service."""
    return CartService(db)


def get_current_customer_id() -> int:
    """
    Dependency to get current authenticated customer ID.

    TODO: Replace with actual auth implementation in TASK-7.
    For now, return a placeholder customer ID.
    """
    return 1  # Placeholder - will be replaced with JWT auth


@router.get("", response_model=CartResponse)
def get_cart(
    customer_id: int = Depends(get_current_customer_id),
    service: CartService = Depends(get_cart_service),
):
    """
    Get current customer's cart with items.

    Requires authentication.
    """
    cart = service.get_cart(customer_id)

    if not cart:
        # Return empty cart
        return CartResponse(
            id=0,
            customer_id=customer_id,
            items=[],
            total_items=0,
            subtotal=Decimal("0.00"),
            created_at="",
            updated_at="",
        )

    # Calculate totals
    total_items, subtotal = service.calculate_cart_totals(cart)

    # Build response
    cart_items = []
    for item in cart.items:
        product = item.product
        product_summary = ProductSummary(
            id=product.id,
            name=product.name,
            brand=product.brand,
            price=product.price,
            sku=product.sku,
            stock_status=None,  # Could compute if needed
        )

        cart_item_response = CartItemResponse(
            id=item.id,
            cart_id=item.cart_id,
            product_id=item.product_id,
            quantity=item.quantity,
            product=product_summary,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
        cart_items.append(cart_item_response)

    return CartResponse(
        id=cart.id,
        customer_id=cart.customer_id,
        items=cart_items,
        total_items=total_items,
        subtotal=subtotal,
        created_at=cart.created_at.isoformat(),
        updated_at=cart.updated_at.isoformat(),
    )


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_cart_item(
    item_data: CartItemCreate,
    customer_id: int = Depends(get_current_customer_id),
    service: CartService = Depends(get_cart_service),
):
    """
    Add item to cart.

    Validates stock availability before adding.
    If item already exists, increments quantity.
    Requires authentication.
    """
    try:
        cart_item = service.add_item(customer_id, item_data)

        # Load product for response
        product = cart_item.product
        product_summary = ProductSummary(
            id=product.id,
            name=product.name,
            brand=product.brand,
            price=product.price,
            sku=product.sku,
            stock_status=None,
        )

        return CartItemResponse(
            id=cart_item.id,
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            product=product_summary,
            created_at=cart_item.created_at.isoformat(),
            updated_at=cart_item.updated_at.isoformat(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.put("/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    customer_id: int = Depends(get_current_customer_id),
    service: CartService = Depends(get_cart_service),
):
    """
    Update cart item quantity.

    Validates stock availability for new quantity.
    Requires authentication.
    """
    try:
        cart_item = service.update_item(customer_id, item_id, item_data)

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        # Load product for response
        product = cart_item.product
        product_summary = ProductSummary(
            id=product.id,
            name=product.name,
            brand=product.brand,
            price=product.price,
            sku=product.sku,
            stock_status=None,
        )

        return CartItemResponse(
            id=cart_item.id,
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            product=product_summary,
            created_at=cart_item.created_at.isoformat(),
            updated_at=cart_item.updated_at.isoformat(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    item_id: int,
    customer_id: int = Depends(get_current_customer_id),
    service: CartService = Depends(get_cart_service),
):
    """
    Remove item from cart.

    Requires authentication.
    """
    success = service.remove_item(customer_id, item_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    return None
