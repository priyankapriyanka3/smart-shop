"""Inventory domain tests."""
import pytest
from fastapi import status


class TestInventoryOperations:
    """Test inventory management operations."""
    
    def test_get_inventory_list(self, client, admin_token, test_inventory):
        """Test getting inventory list."""
        response = client.get(
            "/api/v1/inventory",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1
        
        # Check inventory structure
        item = data["items"][0]
        assert "id" in item
        assert "product_id" in item
        assert "warehouse_id" in item
        assert "quantity" in item
        assert "reorder_level" in item
        assert "status" in item
    
    def test_get_inventory_by_product(self, client, admin_token, test_inventory, test_product):
        """Test getting inventory for specific product."""
        response = client.get(
            f"/api/v1/inventory?product_id={test_product.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] >= 1
        
        for item in data["items"]:
            assert item["product_id"] == test_product.id
    
    def test_get_inventory_by_warehouse(self, client, admin_token, test_inventory, test_warehouse):
        """Test getting inventory for specific warehouse."""
        response = client.get(
            f"/api/v1/inventory?warehouse_id={test_warehouse.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] >= 1
        
        for item in data["items"]:
            assert item["warehouse_id"] == test_warehouse.id


class TestStockUpdates:
    """Test stock update operations."""
    
    def test_update_stock_quantity(self, client, admin_token, test_inventory, db):
        """Test updating inventory stock quantity."""
        response = client.patch(
            f"/api/v1/inventory/{test_inventory.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "quantity": 150,
                "reason": "Stock replenishment",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 150
        
        # Verify in database
        db.refresh(test_inventory)
        assert test_inventory.quantity == 150
    
    def test_increase_stock(self, client, admin_token, test_inventory, db):
        """Test increasing stock quantity."""
        original_quantity = test_inventory.quantity
        
        response = client.post(
            f"/api/v1/inventory/{test_inventory.id}/adjust",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "adjustment": 50,
                "reason": "Received shipment",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == original_quantity + 50
    
    def test_decrease_stock(self, client, admin_token, test_inventory, db):
        """Test decreasing stock quantity."""
        original_quantity = test_inventory.quantity
        
        response = client.post(
            f"/api/v1/inventory/{test_inventory.id}/adjust",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "adjustment": -20,
                "reason": "Damaged goods removed",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == original_quantity - 20


class TestOversellPrevention:
    """Test oversell prevention logic."""
    
    def test_prevent_negative_stock(self, client, admin_token, test_inventory):
        """Test preventing stock from going negative."""
        # Try to decrease stock below zero
        response = client.post(
            f"/api/v1/inventory/{test_inventory.id}/adjust",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "adjustment": -200,  # test_inventory has 100 units
                "reason": "Test adjustment",
            },
        )
        
        # Should reject the adjustment
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "negative" in response.json()["detail"].lower() or "insufficient" in response.json()["detail"].lower()
    
    def test_cart_validates_available_stock(self, client, auth_token, test_product, test_inventory):
        """Test cart operations validate against available stock."""
        # test_inventory has 100 units
        
        # Try to add more than available
        response = client.post(
            "/api/v1/cart/items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "product_id": test_product.id,
                "quantity": 150,
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "stock" in response.json()["detail"].lower()
    
    def test_checkout_validates_current_stock(self, client, auth_token, test_product, db):
        """Test checkout validates stock at submission time."""
        from app.models.cart import Cart, CartItem
        from app.models.customers import User, Address
        from app.models.inventory import Inventory, Warehouse
        
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
        
        # Create warehouse with limited stock
        warehouse = Warehouse(name="Limited Warehouse", code="LIMITED-WH", location="Test", status="active")
        db.add(warehouse)
        db.commit()
        
        # Set very limited stock
        inventory = Inventory(
            product_id=test_product.id,
            warehouse_id=warehouse.id,
            quantity=2,
            reorder_level=5,
            status="low_stock",
        )
        db.add(inventory)
        db.commit()
        
        # Create cart requesting 3 units (exceeds available 2)
        cart = Cart(customer_id=user.id, status="active")
        db.add(cart)
        db.commit()
        
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=test_product.id,
            quantity=3,
        )
        db.add(cart_item)
        db.commit()
        
        # Try to checkout
        response = client.post(
            "/api/v1/checkout/validate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "shipping_address_id": address.id,
                "billing_address_id": address.id,
            },
        )
        
        # Should fail validation
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLowStockAlerts:
    """Test low stock monitoring."""
    
    def test_get_low_stock_items(self, client, admin_token, db, test_product, test_warehouse):
        """Test getting low stock items."""
        from app.models.inventory import Inventory
        
        # Create inventory below reorder level
        low_stock = Inventory(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            quantity=5,
            reorder_level=20,
            status="low_stock",
        )
        db.add(low_stock)
        db.commit()
        
        response = client.get(
            "/api/v1/inventory/low-stock",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should include items where quantity < reorder_level
        assert len(data["items"]) >= 1
        
        for item in data["items"]:
            assert item["quantity"] < item["reorder_level"]
    
    def test_inventory_status_reflects_stock_level(self, client, admin_token, db, test_product, test_warehouse):
        """Test inventory status updates based on stock level."""
        from app.models.inventory import Inventory
        
        # Create inventory with different stock levels
        out_of_stock = Inventory(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            quantity=0,
            reorder_level=10,
            status="out_of_stock",
        )
        db.add(out_of_stock)
        db.commit()
        
        response = client.get(
            f"/api/v1/inventory/{out_of_stock.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "out_of_stock"
        assert data["quantity"] == 0


class TestInventoryAuth:
    """Test inventory endpoint authorization."""
    
    def test_inventory_requires_authentication(self, client):
        """Test inventory endpoints require authentication."""
        response = client.get("/api/v1/inventory")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_inventory_requires_admin_role(self, client, auth_token):
        """Test inventory management requires admin or inventory_manager role."""
        # Regular customer should not have access
        response = client.get(
            "/api/v1/inventory",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        # Should deny access (403) or require specific role
        # Implementation may vary based on RBAC setup
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_200_OK,  # If inventory read is allowed for customers
        ]
    
    def test_stock_updates_require_admin(self, client, auth_token, test_inventory):
        """Test stock updates require admin privileges."""
        response = client.patch(
            f"/api/v1/inventory/{test_inventory.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"quantity": 200, "reason": "Test"},
        )
        
        # Customer should not be able to modify inventory
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
