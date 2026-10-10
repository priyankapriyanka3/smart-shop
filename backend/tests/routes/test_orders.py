"""Tests for order routes."""

import pytest

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.category import Category


@pytest.fixture
def test_customer(test_db):
    """Create a test customer."""
    customer = Customer(
        email="customer@example.com",
        password_hash="hashed_password",
        full_name="Test Customer",
        role="shopper",
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    return customer


@pytest.fixture
def test_order(test_db, test_customer):
    """Create a test order."""
    # Create category and product first
    category = Category(name="Electronics", description="Electronic items", is_active=True)
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    
    product = Product(
        name="Test Product",
        description="A test product",
        brand="TestBrand",
        sku="TEST001",
        price=99.99,
        category_id=category.id,
        is_active="active",
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    
    # Create order
    order = Order(
        customer_id=test_customer.id,
        total_amount=99.99,
        status="pending",
        delivery_address="123 Test St",
    )
    test_db.add(order)
    test_db.commit()
    test_db.refresh(order)
    
    # Create order item
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=1,
        unit_price=99.99,
    )
    test_db.add(order_item)
    test_db.commit()
    
    return order


def test_list_orders(client, test_order, test_customer):
    """Test listing orders for a customer."""
    response = client.get(f"/api/orders/?customer_id={test_customer.id}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


def test_get_order(client, test_order):
    """Test getting a specific order."""
    response = client.get(f"/api/orders/{test_order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_order.id
    assert data["customer_id"] == test_order.customer_id
    assert data["status"] == "pending"


def test_get_order_not_found(client):
    """Test getting a non-existent order."""
    response = client.get("/api/orders/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_update_order_status(client, test_order, test_customer):
    """Test updating order status."""
    response = client.patch(
        f"/api/orders/{test_order.id}/status?actor_id={test_customer.id}",
        json={"status": "confirmed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"


def test_add_order_note(client, test_order, test_customer):
    """Test adding a support note to an order."""
    response = client.post(
        f"/api/orders/{test_order.id}/notes?actor_id={test_customer.id}",
        json={"note": "Customer called to confirm delivery address"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Note added successfully"
