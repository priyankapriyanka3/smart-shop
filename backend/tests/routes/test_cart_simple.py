"""Simplified integration tests for cart routes."""
import pytest
from fastapi import status


def test_cart_workflow(client, sample_customer, sample_product, sample_inventory):
    """Test basic cart add, get, update, remove workflow."""
    # Get empty cart
    get_response = client.get("/api/cart")
    assert get_response.status_code == status.HTTP_200_OK
    cart = get_response.json()
    assert cart["total_items"] == 0
    
    # Add item to cart
    add_data = {"product_id": sample_product.id, "quantity": 2}
    add_response = client.post("/api/cart/items", json=add_data)
    assert add_response.status_code == status.HTTP_201_CREATED
    item = add_response.json()
    assert item["quantity"] == 2
    item_id = item["id"]
    
    # Get cart with items
    get_response = client.get("/api/cart")
    assert get_response.status_code == status.HTTP_200_OK
    cart = get_response.json()
    assert cart["total_items"] == 2
    assert len(cart["items"]) == 1
    
    # Update item quantity
    update_data = {"quantity": 5}
    update_response = client.put(f"/api/cart/items/{item_id}", json=update_data)
    assert update_response.status_code == status.HTTP_200_OK
    updated = update_response.json()
    assert updated["quantity"] == 5
    
    # Remove item
    delete_response = client.delete(f"/api/cart/items/{item_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify cart is empty
    get_response = client.get("/api/cart")
    cart = get_response.json()
    assert len(cart["items"]) == 0
