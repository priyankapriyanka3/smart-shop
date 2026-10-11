"""Cart domain service: Shopping cart management with stock validation."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cart import Cart, CartItem
from app.models.catalog import Product
from app.models.inventory import Inventory
from app.schemas.cart import (
    CartResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
)


class CartService:
    """Service for cart operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_cart(self, customer_id: int) -> Cart:
        """Get active cart for customer or create new one."""
        cart = (
            self.db.query(Cart)
            .filter(Cart.customer_id == customer_id, Cart.status == "active")
            .first()
        )

        if not cart:
            cart = Cart(customer_id=customer_id, status="active")
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)

        return cart

    def get_cart_response(self, cart: Cart) -> CartResponse:
        """Build cart response with enriched item data."""
        items = []
        subtotal = 0.0

        for cart_item in cart.items:
            product = cart_item.product
            item_subtotal = cart_item.quantity * product.price

            items.append(
                CartItemResponse(
                    id=cart_item.id,
                    cart_id=cart_item.cart_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    product_name=product.name,
                    product_price=product.price,
                    product_image_url=product.image_url,
                    subtotal=item_subtotal,
                    created_at=cart_item.created_at,
                    updated_at=cart_item.updated_at,
                )
            )
            subtotal += item_subtotal

        return CartResponse(
            id=cart.id,
            customer_id=cart.customer_id,
            status=cart.status,
            items=items,
            subtotal=subtotal,
            total_items=len(items),
            created_at=cart.created_at,
            updated_at=cart.updated_at,
        )

    def get_cart(self, customer_id: int) -> CartResponse:
        """Get cart for customer."""
        cart = self.get_or_create_cart(customer_id)
        return self.get_cart_response(cart)

    def check_stock_availability(self, product_id: int, quantity: int) -> tuple[bool, int]:
        """Check if product has sufficient stock."""
        available = (
            self.db.query(func.sum(Inventory.quantity))
            .filter(Inventory.product_id == product_id)
            .scalar()
            or 0
        )
        return available >= quantity, available

    def add_item(self, customer_id: int, data: CartItemCreate) -> CartResponse:
        """Add item to cart with stock validation."""
        # Check stock availability
        has_stock, available = self.check_stock_availability(
            data.product_id, data.quantity
        )
        if not has_stock:
            raise ValueError(
                f"Insufficient stock. Available: {available}, Requested: {data.quantity}"
            )

        cart = self.get_or_create_cart(customer_id)

        # Check if item already exists in cart
        existing_item = (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,
                CartItem.product_id == data.product_id,
            )
            .first()
        )

        if existing_item:
            # Update quantity and re-validate stock
            new_quantity = existing_item.quantity + data.quantity
            has_stock, available = self.check_stock_availability(
                data.product_id, new_quantity
            )
            if not has_stock:
                raise ValueError(
                    f"Insufficient stock. Available: {available}, Requested: {new_quantity}"
                )
            existing_item.quantity = new_quantity
        else:
            # Add new item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=data.product_id,
                quantity=data.quantity,
            )
            self.db.add(cart_item)

        self.db.commit()
        self.db.refresh(cart)
        return self.get_cart_response(cart)

    def update_item(
        self,
        customer_id: int,
        cart_item_id: int,
        data: CartItemUpdate,
    ) -> CartResponse:
        """Update cart item quantity with stock validation."""
        cart = self.get_or_create_cart(customer_id)

        cart_item = (
            self.db.query(CartItem)
            .filter(CartItem.id == cart_item_id, CartItem.cart_id == cart.id)
            .first()
        )

        if not cart_item:
            raise ValueError("Cart item not found")

        # Validate stock for new quantity
        has_stock, available = self.check_stock_availability(
            cart_item.product_id, data.quantity
        )
        if not has_stock:
            raise ValueError(
                f"Insufficient stock. Available: {available}, Requested: {data.quantity}"
            )

        cart_item.quantity = data.quantity
        self.db.commit()
        self.db.refresh(cart)
        return self.get_cart_response(cart)

    def remove_item(self, customer_id: int, cart_item_id: int) -> CartResponse:
        """Remove item from cart."""
        cart = self.get_or_create_cart(customer_id)

        cart_item = (
            self.db.query(CartItem)
            .filter(CartItem.id == cart_item_id, CartItem.cart_id == cart.id)
            .first()
        )

        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()

        self.db.refresh(cart)
        return self.get_cart_response(cart)

    def clear_cart(self, customer_id: int) -> CartResponse:
        """Clear all items from cart."""
        cart = self.get_or_create_cart(customer_id)

        self.db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        self.db.commit()
        self.db.refresh(cart)
        return self.get_cart_response(cart)
