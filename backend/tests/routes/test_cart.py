"""Tests for cart routes."""
import pytest
from fastapi import status


def test_get_empty_cart(client, sample_customer):
    """Test getting empty cart."""
    response = client.get("/api/cart")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["items"] == []
    assert data["total_items"] == 0
    assert float(data["subtotal"]) == 0.0


def test_add_item_to_cart(client, sample_customer, sample_product, sample_inventory):
    """Test adding item to cart."""
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 2,
    }

    response = client.post("/api/cart/items", json=cart_item_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["product_id"] == sample_product.id
    assert data["quantity"] == 2
    assert data["product"]["name"] == "Test Product"


def test_add_item_insufficient_stock(client, sample_customer, sample_product, sample_inventory):
    """Test adding item with insufficient stock."""
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 200,  # More than available (100)
    }

    response = client.post("/api/cart/items", json=cart_item_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "insufficient stock" in response.json()["detail"].lower()


def test_add_item_inactive_product(client, test_db, sample_customer, sample_category):
    """Test adding inactive product to cart."""
    from app.models.product import Product

    # Create inactive product
    inactive_product = Product(
        name="Inactive Product",
        description="An inactive product",
        brand="TestBrand",
        sku="INACTIVE-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="inactive",
    )
    test_db.add(inactive_product)
    test_db.commit()
    test_db.refresh(inactive_product)
    product_id = inactive_product.id

    cart_item_data = {
        "product_id": product_id,
        "quantity": 1,
    }

    response = client.post("/api/cart/items", json=cart_item_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_add_duplicate_item_increments_quantity(client, sample_customer, sample_product, sample_inventory):
    """Test adding duplicate item increments quantity."""
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 2,
    }

    # Add first time
    response1 = client.post("/api/cart/items", json=cart_item_data)
    assert response1.status_code == status.HTTP_201_CREATED

    # Add again
    response2 = client.post("/api/cart/items", json=cart_item_data)
    assert response2.status_code == status.HTTP_201_CREATED
    data = response2.json()
    assert data["quantity"] == 4  # 2 + 2


def test_get_cart_with_items(client, sample_customer, sample_product, sample_inventory):
    """Test getting cart with items."""
    # Add item first
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 3,
    }
    client.post("/api/cart/items", json=cart_item_data)

    # Get cart
    response = client.get("/api/cart")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total_items"] == 3
    assert float(data["subtotal"]) == pytest.approx(3 * 99.99, rel=1e-5)


def test_update_cart_item(client, sample_customer, sample_product, sample_inventory):
    """Test updating cart item quantity."""
    # Add item first
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 2,
    }
    add_response = client.post("/api/cart/items", json=cart_item_data)
    item_id = add_response.json()["id"]

    # Update quantity
    update_data = {"quantity": 5}
    response = client.put(f"/api/cart/items/{item_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 5


def test_update_cart_item_insufficient_stock(client, sample_customer, sample_product, sample_inventory):
    """Test updating cart item with insufficient stock."""
    # Add item first
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 2,
    }
    add_response = client.post("/api/cart/items", json=cart_item_data)
    item_id = add_response.json()["id"]

    # Try to update to quantity exceeding stock
    update_data = {"quantity": 200}
    response = client.put(f"/api/cart/items/{item_id}", json=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_cart_item_not_found(client):
    """Test updating non-existent cart item."""
    update_data = {"quantity": 5}
    response = client.put("/api/cart/items/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_remove_cart_item(client, sample_customer, sample_product, sample_inventory):
    """Test removing item from cart."""
    # Add item first
    cart_item_data = {
        "product_id": sample_product.id,
        "quantity": 2,
    }
    add_response = client.post("/api/cart/items", json=cart_item_data)
    item_id = add_response.json()["id"]

    # Remove item
    response = client.delete(f"/api/cart/items/{item_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify cart is empty
    cart_response = client.get("/api/cart")
    assert len(cart_response.json()["items"]) == 0


def test_remove_cart_item_not_found(client):
    """Test removing non-existent cart item."""
    response = client.delete("/api/cart/items/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cart_calculates_totals_correctly(client, test_db, sample_customer, sample_category, sample_warehouse):
    """Test cart calculates totals correctly with multiple items."""
    from app.models.product import Product
    from app.models.inventory import Inventory

    # Create multiple products
    product1 = Product(
        name="Product 1",
        description="Description 1",
        brand="Brand1",
        sku="P1-001",
        price=10.00,
        category_id=sample_category.id,
        is_active="active",
    )
    product2 = Product(
        name="Product 2",
        description="Description 2",
        brand="Brand2",
        sku="P2-001",
        price=25.50,
        category_id=sample_category.id,
        is_active="active",
    )
    test_db.add(product1)
    test_db.add(product2)
    test_db.commit()
    test_db.refresh(product1)
    test_db.refresh(product2)

    # Add inventory
    inv1 = Inventory(product_id=product1.id, warehouse_id=sample_warehouse.id, quantity=100, reorder_level=10)
    inv2 = Inventory(product_id=product2.id, warehouse_id=sample_warehouse.id, quantity=100, reorder_level=10)
    test_db.add(inv1)
    test_db.add(inv2)
    test_db.commit()

    p1_id = product1.id
    p2_id = product2.id

    # Add items to cart
    client.post("/api/cart/items", json={"product_id": p1_id, "quantity": 3})
    client.post("/api/cart/items", json={"product_id": p2_id, "quantity": 2})

    # Get cart and verify totals
    response = client.get("/api/cart")
    data = response.json()
    assert data["total_items"] == 5  # 3 + 2
    assert float(data["subtotal"]) == (3 * 10.00) + (2 * 25.50)  # 30.00 + 51.00 = 81.00
