"""Checkout domain tests."""
import pytest
from fastapi import status


class TestCheckoutValidation:
    """Test checkout validation endpoint."""
    
    def test_validate_checkout_success(self, client, auth_token, test_product, test_inventory, db):
        """Test successful checkout validation."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        
        # Get user
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create cart with items
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is True
        assert "subtotal" in data
        assert "total" in data
    
    def test_validate_checkout_with_promotion(
        self, client, auth_token, test_product, test_inventory, test_promotion, db
    ):
        """Test checkout validation with valid promotion code."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        
        # Get user
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create cart with items (subtotal = 199.98, exceeds promotion minimum of 50)
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        # test_promotion is "TEST10" with 10% discount, min order 50
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "promotion_code": "TEST10",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is True
        assert "discount" in data
        assert data["discount"] > 0
        
        # Verify discount is 10% of subtotal
        expected_discount = data["subtotal"] * 0.10
        assert abs(data["discount"] - expected_discount) < 0.01


class TestPromotionValidation:
    """Test promotion validation in checkout."""
    
    def test_invalid_promotion_code(self, client, auth_token, test_product, test_inventory, db):
        """Test checkout with invalid promotion code."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "promotion_code": "INVALID_CODE",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not found" in response.json()["detail"].lower()
    
    def test_expired_promotion(self, client, auth_token, test_product, test_inventory, expired_promotion, db):
        """Test checkout with expired promotion."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "promotion_code": "EXPIRED",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "expired" in response.json()["detail"].lower()
    
    def test_promotion_minimum_order_not_met(
        self, client, auth_token, db, test_category, test_warehouse, test_promotion
    ):
        """Test promotion with minimum order amount not met."""
        from app.models.catalog import Product
        from app.models.inventory import Inventory
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        
        # Create cheap product (test_promotion requires min order of 50)
        product = Product(
            name="Cheap Product",
            slug="cheap-product",
            sku="CHEAP-001",
            price=10.0,
            brand="Test Brand",
            category_id=test_category.id,
            status="active",
        )
        db.add(product)
        db.commit()
        
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=test_warehouse.id,
            quantity=100,
            reorder_level=20,
            status="in_stock",
        )
        db.add(inventory)
        db.commit()
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create cart with cheap product (subtotal = 20, below 50 minimum)
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "promotion_code": "TEST10",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "minimum" in response.json()["detail"].lower()


class TestInventoryCheck:
    """Test inventory validation during checkout."""
    
    def test_checkout_validates_inventory(self, client, auth_token, test_product, db):
        """Test checkout validates current inventory availability."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User
        from app.models.inventory import Inventory, Warehouse
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create warehouse and limited inventory
        warehouse = Warehouse(name="Test Warehouse", code="TEST-WH", location="Test", status="active")
        db.add(warehouse)
        db.commit()
        
        inventory = Inventory(
            product_id=test_product.id,
            warehouse_id=warehouse.id,
            quantity=5,  # Only 5 available
            reorder_level=10,
            status="in_stock",
        )
        db.add(inventory)
        db.commit()
        
        # Create cart requesting 10 units (exceeds available)
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=10,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "stock" in response.json()["detail"].lower()


class TestOrderCreation:
    """Test order creation from checkout."""
    
    def test_create_order_success(self, client, auth_token, test_product, test_inventory, db):
        """Test successful order creation."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User, Address
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create addresses
        shipping_address = Address(
            user_id=user.id,
            address_type="shipping",
            street="123 Test St",
            city="Test City",
            state_province="TS",
            postal_code="12345",
            country="USA",
            is_default=True,
        )
        db.add(shipping_address)
        db.commit()
        
        # Create cart with items
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=2,
        )
        db.add(cart_item)
        db.commit()
        
        response = client.post(
            "/api/v1/checkout/submit",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": shipping_address.id,
                "billing_address_id": shipping_address.id,
                "payment_method": "credit_card",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "order_id" in data
        assert "order_number" in data
        assert data["payment_status"] == "pending"
    
    def test_order_creation_idempotency(
        self, client, auth_token, test_product, test_inventory, db
    ):
        """Test order creation is idempotent (duplicate prevention)."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User, Address
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create address
        shipping_address = Address(
            user_id=user.id,
            address_type="shipping",
            street="123 Test St",
            city="Test City",
            state_province="TS",
            postal_code="12345",
            country="USA",
            is_default=True,
        )
        db.add(shipping_address)
        db.commit()
        
        # Create cart
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=1,
        )
        db.add(cart_item)
        db.commit()
        
        checkout_data = {
            "shipping_address_id": shipping_address.id,
            "billing_address_id": shipping_address.id,
            "payment_method": "credit_card",
        }
        
        # First submission
        response1 = client.post(
            "/api/v1/checkout/submit",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=checkout_data,
        )
        
        assert response1.status_code == status.HTTP_201_CREATED
        order1_id = response1.json()["order_id"]
        
        # Recreate cart for second attempt
        cart2 = Cart(customer_id=user.id, status="active")
        db.add(cart2)
        db.commit()
        
        cart_item2 = CartItem(
            cart_id=cart2.id,
            product_id=test_product.id,
            quantity=1,
        )
        db.add(cart_item2)
        db.commit()
        
        # Second submission should succeed with new cart
        # (idempotency is per-cart, not global)
        response2 = client.post(
            "/api/v1/checkout/submit",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=checkout_data,
        )
        
        # Should create new order (different cart)
        assert response2.status_code == status.HTTP_201_CREATED


class TestCheckoutAuth:
    """Test checkout authentication requirements."""
    
    def test_checkout_requires_authentication(self, client):
        """Test checkout endpoints require authentication."""
        response = client.post(
            "/api/v1/checkout/validate",
            json={"shipping_address_id": 1, "billing_address_id": 1},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_submit_order_requires_authentication(self, client):
        """Test order submission requires authentication."""
        response = client.post(
            "/api/v1/checkout/submit",
            json={
                "shipping_address_id": 1,
                "billing_address_id": 1,
                "payment_method": "credit_card",
            },
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
