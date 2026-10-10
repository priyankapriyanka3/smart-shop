"""Simplified integration tests for product routes."""
import pytest
from fastapi import status


def test_products_health_check_integration(client, sample_product, sample_inventory):
    """Test basic product list and get functionality."""
    # Test list
    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    
    # Test get by ID
    if len(data["items"]) > 0:
        product_id = data["items"][0]["id"]
        response = client.get(f"/api/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK
        product = response.json()
        assert "name" in product
        assert "price" in product


def test_create_and_activate_product(client, sample_category):
    """Test product creation and activation flow."""
    # Create product
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "brand": "TestBrand",
        "sku": "TEST-SKU",
        "price": 99.99,
        "category_id": sample_category.id,
    }
    
    create_response = client.post("/api/products", json=product_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    assert created["is_active"] == "draft"
    
    # Activate product
    activate_response = client.patch(f"/api/products/{created['id']}/activate")
    assert activate_response.status_code == status.HTTP_200_OK
    activated = activate_response.json()
    assert activated["is_active"] == "active"
