"""Cart domain tests."""
import pytest
from fastapi import status


class TestCartOperations:
    """Test cart CRUD operations."""
    
    def test_get_empty_cart(self, client, auth_token):
        """Test getting empty cart creates new cart."""
        response = client.get(
            "/api/v1/cart",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert "items" in data
        assert len(data["items"]) == 0
        assert data["subtotal"] == 0.0
        assert data["total_items"] == 0
    
    def test_add_item_to_cart(self, client, auth_token, test_product, test_inventory):
        """Test adding item to cart with stock validation."""
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "product_id": test_product.id,
                "quantity": 2,
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == test_product.id
        assert data["items"][0]["quantity"] == 2
        assert data["items"][0]["product_name"] == test_product.name
        assert data["items"][0]["product_price"] == test_product.price
        assert data["subtotal"] == test_product.price * 2
        assert data["total_items"] == 1
    
    def test_add_multiple_items(self, client, auth_token, db, test_category, test_warehouse):
        """Test adding multiple different items to cart."""
        from app.models.catalog import Product
        from app.models.inventory import Inventory
        
        # Create two products with inventory
        products = []
        for i in range(2):
            product = Product(
                name=f"Product {i}",
                slug=f"product-{i}",
                sku=f"MULTI-{i:03d}",
                price=50.0 + i * 10,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=test_warehouse.id,
                quantity=100,
                reorder_level=20,
                status="in_stock",
            )
            db.add(inventory)
            products.append(product)
        db.commit()
        
        # Add first product
        client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": products[0].id, "quantity": 1},
        )
        
        # Add second product
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": products[1].id, "quantity": 3},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total_items"] == 2
        
        # Check subtotal calculation
        expected_subtotal = products[0].price * 1 + products[1].price * 3
        assert abs(data["subtotal"] - expected_subtotal) < 0.01


class TestCartItemUpdate:
    """Test cart item quantity updates."""
    
    def test_update_item_quantity(self, client, auth_token, test_product, test_inventory):
        """Test updating cart item quantity."""
        # Add item first
        add_response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 2},
        )
        cart_item_id = add_response.json()["items"][0]["id"]
        
        # Update quantity
        response = client.patch(
            f"/api/v1/cart/items/{cart_item_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"quantity": 5},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 5
        assert data["subtotal"] == test_product.price * 5
    
    def test_update_quantity_to_zero_removes_item(self, client, auth_token, test_product, test_inventory):
        """Test updating quantity to zero removes item."""
        # Add item first
        add_response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 2},
        )
        cart_item_id = add_response.json()["items"][0]["id"]
        
        # Update quantity to 1 (minimum valid quantity)
        response = client.patch(
            f"/api/v1/cart/items/{cart_item_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"quantity": 1},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"][0]["quantity"] == 1


class TestCartItemRemove:
    """Test removing items from cart."""
    
    def test_remove_item_from_cart(self, client, auth_token, test_product, test_inventory):
        """Test removing item from cart."""
        # Add item first
        add_response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 2},
        )
        cart_item_id = add_response.json()["items"][0]["id"]
        
        # Remove item
        response = client.delete(
            f"/api/v1/cart/items/{cart_item_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 0
        assert data["subtotal"] == 0.0
        assert data["total_items"] == 0
    
    def test_remove_nonexistent_item(self, client, auth_token):
        """Test removing non-existent cart item."""
        response = client.delete(
            "/api/v1/cart/items/99999",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        # Should return success (idempotent) with empty cart
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 0


class TestStockValidation:
    """Test stock validation for cart operations."""
    
    def test_add_item_insufficient_stock(self, client, auth_token, test_product, test_inventory):
        """Test adding item with quantity exceeding available stock."""
        # test_inventory has quantity=100
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 150},
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in response.json()["detail"]
        assert "Available: 100" in response.json()["detail"]
    
    def test_add_item_no_inventory(self, client, auth_token, db, test_category):
        """Test adding item with no inventory records."""
        from app.models.catalog import Product
        
        # Create product without inventory
        product = Product(
            name="No Stock Product",
            slug="no-stock-product",
            sku="NOSTOCK-001",
            price=99.99,
            brand="Test Brand",
            category_id=test_category.id,
            status="active",
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": product.id, "quantity": 1},
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in response.json()["detail"]
        assert "Available: 0" in response.json()["detail"]
    
    def test_update_item_insufficient_stock(self, client, auth_token, test_product, test_inventory):
        """Test updating item quantity beyond available stock."""
        # Add item first with valid quantity
        add_response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 10},
        )
        cart_item_id = add_response.json()["items"][0]["id"]
        
        # Try to update to quantity exceeding stock
        response = client.patch(
            f"/api/v1/cart/items/{cart_item_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"quantity": 150},
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in response.json()["detail"]
    
    def test_add_same_item_twice_validates_total(self, client, auth_token, test_product, test_inventory):
        """Test adding same item multiple times validates cumulative quantity."""
        # Add item with 60 units
        client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 60},
        )
        
        # Try to add 50 more (total would be 110, but stock is 100)
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"product_id": test_product.id, "quantity": 50},
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in response.json()["detail"]


class TestCartAuth:
    """Test cart authentication requirements."""
    
    def test_cart_requires_authentication(self, client):
        """Test cart endpoints require authentication."""
        response = client.get("/api/v1/cart")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_add_item_requires_authentication(self, client, test_product):
        """Test adding item requires authentication."""
        response = client.post(
            "/api/v1/cart/items",
            json={"product_id": test_product.id, "quantity": 1},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
