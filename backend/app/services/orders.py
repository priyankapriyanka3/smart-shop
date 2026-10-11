"""Orders domain service: Order creation and management with idempotency."""
import secrets
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.orders import Order, OrderItem
from app.models.cart import Cart
from app.schemas.orders import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderItemResponse,
)


class OrderService:
    """Service for order operations."""

    def __init__(self, db: Session):
        self.db = db

    def generate_order_number(self) -> str:
        """Generate unique order number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = secrets.token_hex(4).upper()
        return f"ORD-{timestamp}-{random_suffix}"

    def create_order(self, data: OrderCreate) -> OrderResponse:
        """Create order from validated checkout data."""
        # Generate unique order number
        order_number = self.generate_order_number()

        # Create order
        order = Order(
            customer_id=data.customer_id,
            order_number=order_number,
            status="placed",
            subtotal=data.subtotal,
            discount_amount=data.discount_amount,
            shipping_cost=data.shipping_cost,
            total=data.total,
            shipping_street=data.shipping_street,
            shipping_city=data.shipping_city,
            shipping_state_province=data.shipping_state_province,
            shipping_postal_code=data.shipping_postal_code,
            shipping_country=data.shipping_country,
            billing_street=data.billing_street,
            billing_city=data.billing_city,
            billing_state_province=data.billing_state_province,
            billing_postal_code=data.billing_postal_code,
            billing_country=data.billing_country,
            promotion_code=data.promotion_code,
        )

        self.db.add(order)
        self.db.flush()  # Get order ID without committing

        # Get customer's active cart
        cart = (
            self.db.query(Cart)
            .filter(Cart.customer_id == data.customer_id, Cart.status == "active")
            .first()
        )

        if cart and cart.items:
            # Create order items from cart
            for cart_item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price,
                    total_price=cart_item.quantity * cart_item.product.price,
                )
                self.db.add(order_item)

            # Mark cart as converted
            cart.status = "converted"

        self.db.commit()
        self.db.refresh(order)

        return self.get_order_response(order)

    def get_order_response(self, order: Order) -> OrderResponse:
        """Build order response with enriched item data."""
        items = []
        for order_item in order.items:
            product = order_item.product
            items.append(
                OrderItemResponse(
                    id=order_item.id,
                    order_id=order_item.order_id,
                    product_id=order_item.product_id,
                    quantity=order_item.quantity,
                    unit_price=order_item.unit_price,
                    total_price=order_item.total_price,
                    product_name=product.name,
                    product_sku=product.sku,
                    created_at=order_item.created_at,
                    updated_at=order_item.updated_at,
                )
            )

        return OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            order_number=order.order_number,
            status=order.status,
            subtotal=order.subtotal,
            discount_amount=order.discount_amount,
            shipping_cost=order.shipping_cost,
            total=order.total,
            shipping_street=order.shipping_street,
            shipping_city=order.shipping_city,
            shipping_state_province=order.shipping_state_province,
            shipping_postal_code=order.shipping_postal_code,
            shipping_country=order.shipping_country,
            billing_street=order.billing_street,
            billing_city=order.billing_city,
            billing_state_province=order.billing_state_province,
            billing_postal_code=order.billing_postal_code,
            billing_country=order.billing_country,
            promotion_code=order.promotion_code,
            items=items,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    def get_orders(
        self,
        customer_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> OrderListResponse:
        """Get paginated list of orders."""
        query = self.db.query(Order)

        if customer_id:
            query = query.filter(Order.customer_id == customer_id)

        if status:
            query = query.filter(Order.status == status)

        query = query.order_by(Order.created_at.desc())

        total = query.count()
        offset = (page - 1) * page_size
        orders = query.offset(offset).limit(page_size).all()

        return OrderListResponse(
            items=[self.get_order_response(order) for order in orders],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_order_by_id(self, order_id: int) -> Optional[OrderResponse]:
        """Get order by ID."""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        return self.get_order_response(order) if order else None

    def get_order_by_number(self, order_number: str) -> Optional[OrderResponse]:
        """Get order by order number."""
        order = self.db.query(Order).filter(Order.order_number == order_number).first()
        return self.get_order_response(order) if order else None

    def update_order_status(self, order_id: int, status: str, user_id: Optional[int] = None) -> Optional[OrderResponse]:
        """Update order status with audit logging."""
        from app.audit.logger import log_audit
        
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None

        old_status = order.status
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        
        # Log audit entry for status change
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="order",
                object_id=order_id,
                action="status_update",
                summary=f"Order {order.order_number} status changed from {old_status} to {status}",
            )
        
        return self.get_order_response(order)
