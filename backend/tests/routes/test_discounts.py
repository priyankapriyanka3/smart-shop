"""Tests for discount routes."""

import pytest
from datetime import datetime, timedelta

from app.models.discount import Discount
from app.models.customer import Customer


@pytest.fixture
def test_actor(test_db):
    """Create test actor."""
    customer = Customer(
        email="admin@example.com",
        password_hash="hashed",
        full_name="Admin User",
        role="admin",
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    return customer


@pytest.fixture
def test_discount(test_db, test_actor):
    """Create a test discount."""
    now = datetime.utcnow()
    discount = Discount(
        code="SAVE10",
        discount_type="percentage",
        discount_value=10.0,
        min_order_amount=50.0,
        valid_from=now - timedelta(days=1),
        valid_to=now + timedelta(days=30),
        max_uses=100,
        times_used=0,
        is_active=True,
    )
    test_db.add(discount)
    test_db.commit()
    test_db.refresh(discount)
    return discount


def test_list_discounts(client, test_discount):
    """Test listing discounts."""
    response = client.get("/api/discounts/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] >= 1


def test_create_discount(client, test_actor):
    """Test creating a discount."""
    now = datetime.utcnow()
    response = client.post(
        f"/api/discounts/?actor_id={test_actor.id}",
        json={
            "code": "NEWCODE",
            "discount_type": "fixed_amount",
            "discount_value": 5.0,
            "min_order_amount": 25.0,
            "valid_from": now.isoformat(),
            "valid_to": (now + timedelta(days=30)).isoformat(),
            "max_uses": 50,
            "is_active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "NEWCODE"


def test_validate_discount_success(client, test_discount):
    """Test validating a valid discount."""
    response = client.post(
        "/api/discounts/validate",
        json={"code": "SAVE10", "cart_total": 100.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert float(data["discount_value"]) == 10.0


def test_validate_discount_min_order(client, test_discount):
    """Test validating discount with insufficient cart total."""
    response = client.post(
        "/api/discounts/validate",
        json={"code": "SAVE10", "cart_total": 30.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "Minimum order amount" in data["error"]


def test_validate_discount_not_found(client):
    """Test validating non-existent discount."""
    response = client.post(
        "/api/discounts/validate",
        json={"code": "INVALID", "cart_total": 100.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "not found" in data["error"]
