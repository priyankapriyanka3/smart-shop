"""Order domain tests."""
import pytest
from fastapi import status


class TestOrderCreation:
    """Test order creation."""
    
    def test_create_order_from_cart(self, client, auth_token, test_product, test_inventory, db):
        """Test creating order from cart."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User, Address
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create address
        address = Address(
            user_id=user.id,
            address_type="shipping",
            street="123 Test St",
            city="Test City",
            state_province="TS",
            postal_code="12345",
            country="USA",
            is_default=True,
        )
        db.add(address)
        db.commit()
        
        # Create cart
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
        
        # Submit checkout
        response = client.post(
            "/api/v1/checkout/submit",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": address.id,
                "billing_address_id": address.id,
                "payment_method": "credit_card",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "order_id" in data
        assert data["payment_status"] == "pending"


class TestOrderHistory:
    """Test order history retrieval."""
    
    def test_get_order_history(self, client, auth_token, db):
        """Test getting order history for customer."""
        from app.models.customers import User
        from app.models.orders import Order
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create test orders
        for i in range(3):
            order = Order(
                customer_id=user.id,
                order_number=f"SS-TEST-{i:06d}",
                status="pending",
                subtotal=100.0 + i * 10,
                discount_amount=0.0,
                shipping_cost=10.0,
                total=110.0 + i * 10,
                shipping_street="123 Test St",
                shipping_city="Test City",
                shipping_state_province="TS",
                shipping_postal_code="12345",
                shipping_country="USA",
                billing_street="123 Test St",
                billing_city="Test City",
                billing_state_province="TS",
                billing_postal_code="12345",
                billing_country="USA",
            )
            db.add(order)
        db.commit()
        
        response = client.get(
            "/api/v1/orders",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3
    
    def test_get_order_history_pagination(self, client, auth_token, db):
        """Test order history pagination."""
        from app.models.customers import User
        from app.models.orders import Order
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create 15 orders
        for i in range(15):
            order = Order(
                customer_id=user.id,
                order_number=f"SS-PAGE-{i:06d}",
                status="pending",
                subtotal=100.0,
                discount_amount=0.0,
                shipping_cost=10.0,
                total=110.0,
                shipping_street="123 Test St",
                shipping_city="Test City",
                shipping_state_province="TS",
                shipping_postal_code="12345",
                shipping_country="USA",
                billing_street="123 Test St",
                billing_city="Test City",
                billing_state_province="TS",
                billing_postal_code="12345",
                billing_country="USA",
            )
            db.add(order)
        db.commit()
        
        # Get first page
        response = client.get(
            "/api/v1/orders?page=1&page_size=10",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 1
        assert data["total"] >= 15
    
    def test_order_history_only_shows_own_orders(self, client, auth_token, db):
        """Test customers only see their own orders."""
        from app.models.customers import User
        from app.models.orders import Order
        
        # Get test user
        user1 = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create another user
        from app.auth.password import hash_password
        from app.models.admin import Role, UserRole
        
        customer_role = db.query(Role).filter(Role.name == "customer").first()
        if not customer_role:
            customer_role = Role(name="customer", description="Customer")
            db.add(customer_role)
            db.commit()
        
        user2 = User(
            email="other@example.com",
            name="Other User",
            password_hash=hash_password("password"),
            status="active",
            is_deleted=False,
        )
        db.add(user2)
        db.commit()
        
        user_role = UserRole(user_id=user2.id, role_id=customer_role.id)
        db.add(user_role)
        db.commit()
        
        # Create orders for both users
        order1 = Order(
            customer_id=user1.id,
            order_number="SS-USER1-001",
            status="pending",
            subtotal=100.0,
            discount_amount=0.0,
            shipping_cost=10.0,
            total=110.0,
            shipping_street="123 Test St",
            shipping_city="Test City",
            shipping_state_province="TS",
            shipping_postal_code="12345",
            shipping_country="USA",
            billing_street="123 Test St",
            billing_city="Test City",
            billing_state_province="TS",
            billing_postal_code="12345",
            billing_country="USA",
        )
        db.add(order1)
        
        order2 = Order(
            customer_id=user2.id,
            order_number="SS-USER2-001",
            status="pending",
            subtotal=200.0,
            discount_amount=0.0,
            shipping_cost=10.0,
            total=210.0,
            shipping_street="456 Other St",
            shipping_city="Other City",
            shipping_state_province="OS",
            shipping_postal_code="54321",
            shipping_country="USA",
            billing_street="456 Other St",
            billing_city="Other City",
            billing_state_province="OS",
            billing_postal_code="54321",
            billing_country="USA",
        )
        db.add(order2)
        db.commit()
        
        # Get orders for user1
        response = client.get(
            "/api/v1/orders",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should only see user1's orders
        order_numbers = [order["order_number"] for order in data["items"]]
        assert "SS-USER1-001" in order_numbers
        assert "SS-USER2-001" not in order_numbers


class TestOrderDetail:
    """Test order detail retrieval."""
    
    def test_get_order_detail(self, client, auth_token, db, test_product):
        """Test getting order detail."""
        from app.models.customers import User
        from app.models.orders import Order, OrderItem
        
        user = db.query(User).filter(User.email == "test@example.com").first()
        
        # Create order
        order = Order(
            customer_id=user.id,
            order_number="SS-DETAIL-001",
            status="pending",
            subtotal=199.98,
            discount_amount=0.0,
            shipping_cost=10.0,
            total=209.98,
            shipping_street="123 Test St",
            shipping_city="Test City",
            shipping_state_province="TS",
            shipping_postal_code="12345",
            shipping_country="USA",
            billing_street="123 Test St",
            billing_city="Test City",
            billing_state_province="TS",
            billing_postal_code="12345",
            billing_country="USA",
        )
        db.add(order)
        db.commit()
        
        # Add order items
        order_item = OrderItem(
            order_id=order.id,
            product_id=test_product.id,
            quantity=2,
            unit_price=test_product.price,
            total_price=test_product.price * 2,
        )
        db.add(order_item)
        db.commit()
        
        response = client.get(
            f"/api/v1/orders/{order.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == order.id
        assert data["order_number"] == "SS-DETAIL-001"
        assert data["status"] == "pending"
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == test_product.id
        assert data["items"][0]["quantity"] == 2


class TestOrderAuthorization:
    """Test order authorization."""
    
    def test_unauthorized_access_returns_403(self, client, db):
        """Test accessing another customer's order returns 403."""
        from app.models.customers import User
        from app.models.orders import Order
        from app.auth.password import hash_password
        from app.models.admin import Role, UserRole
        
        # Create two users
        customer_role = db.query(Role).filter(Role.name == "customer").first()
        if not customer_role:
            customer_role = Role(name="customer", description="Customer")
            db.add(customer_role)
            db.commit()
        
        user1 = User(
            email="user1@example.com",
            name="User 1",
            password_hash=hash_password("password"),
            status="active",
            is_deleted=False,
        )
        db.add(user1)
        db.commit()
        
        user_role1 = UserRole(user_id=user1.id, role_id=customer_role.id)
        db.add(user_role1)
        
        user2 = User(
            email="user2@example.com",
            name="User 2",
            password_hash=hash_password("password"),
            status="active",
            is_deleted=False,
        )
        db.add(user2)
        db.commit()
        
        user_role2 = UserRole(user_id=user2.id, role_id=customer_role.id)
        db.add(user_role2)
        db.commit()
        
        # Create order for user2
        order = Order(
            customer_id=user2.id,
            order_number="SS-AUTH-001",
            status="pending",
            subtotal=100.0,
            discount_amount=0.0,
            shipping_cost=10.0,
            total=110.0,
            shipping_street="123 Test St",
            shipping_city="Test City",
            shipping_state_province="TS",
            shipping_postal_code="12345",
            shipping_country="USA",
            billing_street="123 Test St",
            billing_city="Test City",
            billing_state_province="TS",
            billing_postal_code="12345",
            billing_country="USA",
        )
        db.add(order)
        db.commit()
        
        # Login as user1
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "user1@example.com", "password": "password"},
        )
        token = login_response.json()["access_token"]
        
        # Try to access user2's order
        response = client.get(
            f"/api/v1/orders/{order.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        # Should return 403 or 404 (not found for security)
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]


class TestOrderAuth:
    """Test order endpoint authentication."""
    
    def test_orders_require_authentication(self, client):
        """Test order endpoints require authentication."""
        response = client.get("/api/v1/orders")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_order_detail_requires_authentication(self, client):
        """Test order detail requires authentication."""
        response = client.get("/api/v1/orders/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
