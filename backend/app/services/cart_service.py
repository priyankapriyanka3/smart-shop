"""Cart service for shopping cart operations."""
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate


class CartService:
    """Service for cart operations."""

    def __init__(self, db: Session):
        """Initialize cart service."""
        self.db = db

    def get_or_create_cart(self, customer_id: int) -> Cart:
        """Get existing cart or create new one for customer."""
        cart = self.db.query(Cart).filter(Cart.customer_id == customer_id).first()

        if not cart:
            cart = Cart(customer_id=customer_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)

        return cart

    def get_cart(self, customer_id: int) -> Cart | None:
        """Get cart for customer with items."""
        cart = (
            self.db.query(Cart)
            .filter(Cart.customer_id == customer_id)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
            .first()
        )
        return cart

    def _check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available."""
        total_stock = (
            self.db.query(func.sum(Inventory.quantity))
            .filter(Inventory.product_id == product_id)
            .scalar()
        )

        return total_stock is not None and total_stock >= quantity

    def add_item(self, customer_id: int, item_data: CartItemCreate) -> CartItem:
        """Add item to cart."""
        # Verify product exists and is active
        product = (
            self.db.query(Product)
            .filter(Product.id == item_data.product_id, Product.is_active == "active")
            .first()
        )

        if not product:
            raise ValueError("Product not found or not active")

        # Check stock availability
        if not self._check_stock_availability(item_data.product_id, item_data.quantity):
            raise ValueError("Insufficient stock available")

        # Get or create cart
        cart = self.get_or_create_cart(customer_id)

        # Check if item already in cart
        existing_item = (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == item_data.product_id)
            .first()
        )

        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + item_data.quantity
            if not self._check_stock_availability(item_data.product_id, new_quantity):
                raise ValueError("Insufficient stock for requested quantity")

            existing_item.quantity = new_quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
            )
            self.db.add(cart_item)
            self.db.commit()
            self.db.refresh(cart_item)
            return cart_item

    def update_item(
        self, customer_id: int, item_id: int, item_data: CartItemUpdate
    ) -> CartItem | None:
        """Update cart item quantity."""
        cart = self.get_cart(customer_id)
        if not cart:
            return None

        cart_item = (
            self.db.query(CartItem)
            .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
            .first()
        )

        if not cart_item:
            return None

        # Check stock availability for new quantity
        if not self._check_stock_availability(cart_item.product_id, item_data.quantity):
            raise ValueError("Insufficient stock for requested quantity")

        cart_item.quantity = item_data.quantity
        self.db.commit()
        self.db.refresh(cart_item)

        return cart_item

    def remove_item(self, customer_id: int, item_id: int) -> bool:
        """Remove item from cart."""
        cart = self.get_cart(customer_id)
        if not cart:
            return False

        cart_item = (
            self.db.query(CartItem)
            .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
            .first()
        )

        if not cart_item:
            return False

        self.db.delete(cart_item)
        self.db.commit()

        return True

    def clear_cart(self, customer_id: int) -> bool:
        """Clear all items from cart."""
        cart = self.get_cart(customer_id)
        if not cart:
            return False

        self.db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        self.db.commit()

        return True

    def calculate_cart_totals(self, cart: Cart) -> tuple[int, Decimal]:
        """Calculate total items and subtotal for cart."""
        total_items = 0
        subtotal = Decimal("0.00")

        for item in cart.items:
            total_items += item.quantity
            subtotal += item.product.price * item.quantity

        return total_items, subtotal
