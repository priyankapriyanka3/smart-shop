"""Tests for product routes."""
import pytest
from fastapi import status


def test_list_products_empty(client, sample_customer):
    """Test listing products with empty database."""
    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 0
    assert "items" in data


def test_list_products_with_data(client, sample_product, sample_inventory):
    """Test listing products with sample data."""
    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Test Product"
    assert data["items"][0]["stock_status"] == "in_stock"


def test_list_products_pagination(client, test_db, sample_category):
    """Test product pagination."""
    from app.models.product import Product

    # Create multiple products
    for i in range(25):
        product = Product(
            name=f"Product {i}",
            description=f"Description {i}",
            brand="TestBrand",
            sku=f"TEST-{i:03d}",
            price=10.0 + i,
            category_id=sample_category.id,
            is_active="active",
        )
        test_db.add(product)
    test_db.commit()

    # Test page 1
    response = client.get("/api/products?page=1&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["pages"] == 3

    # Test page 2
    response = client.get("/api/products?page=2&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 10


def test_get_product_by_id(client, sample_product, sample_inventory):
    """Test getting product by ID."""
    response = client.get(f"/api/products/{sample_product.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_product.id
    assert data["name"] == "Test Product"
    assert data["sku"] == "TEST-001"
    assert data["stock_status"] == "in_stock"


def test_get_product_not_found(client, sample_customer):
    """Test getting non-existent product."""
    response = client.get("/api/products/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_create_product(client, sample_category):
    """Test creating a new product."""
    product_data = {
        "name": "New Product",
        "description": "A new test product",
        "brand": "NewBrand",
        "sku": "NEW-001",
        "price": 149.99,
        "category_id": sample_category.id,
    }

    response = client.post("/api/products", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Product"
    assert data["is_active"] == "draft"  # Starts in draft state
    assert "id" in data


def test_create_product_invalid_category(client, sample_customer):
    """Test creating product with invalid category."""
    product_data = {
        "name": "New Product",
        "description": "A new test product",
        "brand": "NewBrand",
        "sku": "NEW-001",
        "price": 149.99,
        "category_id": 999,  # Non-existent category
    }

    response = client.post("/api/products", json=product_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_product(client, sample_product):
    """Test updating a product."""
    update_data = {
        "name": "Updated Product Name",
        "price": 129.99,
    }

    response = client.put(f"/api/products/{sample_product.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product Name"
    assert float(data["price"]) == 129.99
    assert data["brand"] == "TestBrand"  # Unchanged


def test_update_product_not_found(client, sample_customer):
    """Test updating non-existent product."""
    update_data = {"name": "Updated Name"}

    response = client.put("/api/products/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_activate_product(client, test_db, sample_category):
    """Test activating a product."""
    from app.models.product import Product

    # Create draft product
    product = Product(
        name="Draft Product",
        description="A draft product",
        brand="DraftBrand",
        sku="DRAFT-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="draft",
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    product_id = product.id

    response = client.patch(f"/api/products/{product_id}/activate")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] == "active"


def test_deactivate_product(client, sample_product):
    """Test deactivating a product."""
    response = client.patch(f"/api/products/{sample_product.id}/deactivate")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] == "inactive"


def test_filter_products_by_category(client, sample_product):
    """Test filtering products by category."""
    response = client.get(f"/api/products?category_id={sample_product.category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["category_id"] == sample_product.category_id
