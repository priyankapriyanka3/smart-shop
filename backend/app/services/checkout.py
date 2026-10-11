"""Checkout domain service: Validation orchestration."""
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.customers import Address
from app.services.cart import CartService
from app.services.promotions import PromotionService
from app.services.orders import OrderService
from app.services.payments import PaymentService
from app.schemas.checkout import CheckoutRequest, CheckoutValidationResponse, CheckoutResponse
from app.schemas.orders import OrderCreate


class CheckoutService:
    """Service for checkout validation orchestration."""

    def __init__(self, db: Session):
        self.db = db
        self.cart_service = CartService(db)
        self.promotion_service = PromotionService(db)
        self.order_service = OrderService(db)
        self.payment_service = PaymentService(db)

    def validate_checkout(
        self,
        customer_id: int,
        request: CheckoutRequest,
    ) -> CheckoutValidationResponse:
        """Validate checkout: inventory, promotions, pricing."""
        errors = []
        inventory_issues = []

        # Get cart
        cart_response = self.cart_service.get_cart(customer_id)
        if not cart_response.items:
            errors.append("Cart is empty")
            return CheckoutValidationResponse(
                valid=False,
                errors=errors,
            )

        # Validate inventory for all items
        for item in cart_response.items:
            has_stock, available = self.cart_service.check_stock_availability(
                item.product_id, item.quantity
            )
            if not has_stock:
                inventory_issues.append(
                    {
                        "product_id": item.product_id,
                        "product_name": item.product_name,
                        "requested": item.quantity,
                        "available": available,
                    }
                )

        if inventory_issues:
            # Raise ValueError for inventory errors to return 400 status
            raise ValueError("Some items have insufficient stock")

        # Calculate subtotal
        subtotal = cart_response.subtotal

        # Validate and apply promotion if provided
        promotion_valid = True
        discount_amount = 0.0

        if request.promotion_code:
            eligibility = self.promotion_service.check_eligibility(
                request.promotion_code,
                subtotal,
            )
            promotion_valid = eligibility.eligible
            discount_amount = eligibility.discount_amount

            if not eligibility.eligible:
                # Raise ValueError for promotion errors to return 400 status
                raise ValueError("; ".join(eligibility.errors))

        # Calculate shipping (fixed for now, could be dynamic)
        shipping_cost = 0.0 if discount_amount > 0 else 9.99

        # Calculate total
        total = subtotal - discount_amount + shipping_cost

        return CheckoutValidationResponse(
            valid=len(errors) == 0,
            errors=errors,
            inventory_issues=inventory_issues,
            promotion_valid=promotion_valid,
            promotion_discount=discount_amount,
            subtotal=subtotal,
            discount_amount=discount_amount,
            discount=discount_amount,
            shipping_cost=shipping_cost,
            total=total,
        )

    def process_checkout(
        self,
        customer_id: int,
        request: CheckoutRequest,
    ) -> CheckoutResponse:
        """Process checkout and create order."""
        # First validate
        validation = self.validate_checkout(customer_id, request)
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))

        # Resolve addresses
        shipping_address = None
        billing_address = None

        if request.shipping_address:
            shipping_address = request.shipping_address
        elif request.shipping_address_id:
            addr = self.db.query(Address).filter(Address.id == request.shipping_address_id).first()
            if addr:
                from app.schemas.checkout import CheckoutAddress
                shipping_address = CheckoutAddress(
                    street=addr.street,
                    city=addr.city,
                    state_province=addr.state_province,
                    postal_code=addr.postal_code,
                    country=addr.country,
                )

        if request.billing_address:
            billing_address = request.billing_address
        elif request.billing_address_id:
            addr = self.db.query(Address).filter(Address.id == request.billing_address_id).first()
            if addr:
                from app.schemas.checkout import CheckoutAddress
                billing_address = CheckoutAddress(
                    street=addr.street,
                    city=addr.city,
                    state_province=addr.state_province,
                    postal_code=addr.postal_code,
                    country=addr.country,
                )

        # Use shipping address for billing if not provided
        if not billing_address and shipping_address:
            billing_address = shipping_address

        # Create order
        order_data = OrderCreate(
            customer_id=customer_id,
            subtotal=validation.subtotal,
            discount_amount=validation.discount_amount,
            shipping_cost=validation.shipping_cost,
            total=validation.total,
            shipping_street=shipping_address.street if shipping_address else "",
            shipping_city=shipping_address.city if shipping_address else "",
            shipping_state_province=shipping_address.state_province if shipping_address else "",
            shipping_postal_code=shipping_address.postal_code if shipping_address else "",
            shipping_country=shipping_address.country if shipping_address else "",
            billing_street=billing_address.street if billing_address else "",
            billing_city=billing_address.city if billing_address else "",
            billing_state_province=billing_address.state_province if billing_address else "",
            billing_postal_code=billing_address.postal_code if billing_address else "",
            billing_country=billing_address.country if billing_address else "",
            promotion_code=request.promotion_code,
        )

        order = self.order_service.create_order(order_data)

        # Create payment record
        payment_method = request.payment_method or "card"
        from app.schemas.payments import PaymentCreate
        payment_data = PaymentCreate(
            order_id=order.id,
            payment_method=payment_method,
            amount=validation.total,
            status="pending",
        )
        payment = self.payment_service.create_payment(payment_data)

        return CheckoutResponse(
            order_id=order.id,
            order_number=order.order_number,
            subtotal=validation.subtotal,
            discount_amount=validation.discount_amount,
            shipping_cost=validation.shipping_cost,
            total=validation.total,
            payment_status=payment.status,
            message="Order created successfully",
        )
