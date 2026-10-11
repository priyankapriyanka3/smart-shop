"""Cross-stack API integration tests.

These tests verify:
1. Backend API endpoints work correctly
2. Response formats match frontend expectations
3. Data contracts are maintained between frontend and backend
4. API serves on expected endpoints that frontend will call
"""
import pytest
from fastapi import status


class TestProductCatalogIntegration:
    """Integration tests for Product Catalog API (Epic 1)."""

    def test_list_products_api_contract(self, client, sample_product, sample_inventory):
        """Verify /api/products response matches frontend expectations."""
        response = client.get("/api/products")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify pagination structure
        assert "items" in data, "Response should include 'items' array"
        assert "total" in data, "Response should include 'total' count"
        assert "pages" in data, "Response should include 'pages' count"
        assert "page" in data, "Response should include current 'page'"
        assert "per_page" in data, "Response should include 'per_page' size"
        
        # Verify product item structure
        if len(data["items"]) > 0:
            product = data["items"][0]
            required_fields = [
                "id", "name", "description", "price", "sku", 
                "brand", "category_id", "is_active", "stock_status"
            ]
            for field in required_fields:
                assert field in product, f"Product should include '{field}' field"

    def test_get_product_by_id_api_contract(self, client, sample_product, sample_inventory):
        """Verify /api/products/{id} response matches frontend expectations."""
        response = client.get(f"/api/products/{sample_product.id}")
        
        assert response.status_code == status.HTTP_200_OK
        product = response.json()
        
        # Verify all required fields for product detail view
        required_fields = [
            "id", "name", "description", "price", "sku", 
            "brand", "category_id", "is_active", "stock_status"
        ]
        for field in required_fields:
            assert field in product, f"Product detail should include '{field}' field"
        
        # Verify data types
        assert isinstance(product["id"], int), "Product ID should be integer"
        assert isinstance(product["price"], (int, float, str)), "Price should be numeric or string"
        assert isinstance(product["is_active"], str), "is_active should be string"
        assert product["stock_status"] in ["in_stock", "low_stock", "out_of_stock"], \
            "stock_status should be valid enum value"

    def test_product_pagination_works_correctly(self, client, test_db, sample_category):
        """Verify pagination parameters work as expected by frontend."""
        from app.models.product import Product
        
        # Create 15 test products
        for i in range(15):
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
        
        # Test page 1 with 10 items per page
        response = client.get("/api/products?page=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10, "Should return 10 items on page 1"
        assert data["page"] == 1
        assert data["total"] == 15
        assert data["pages"] == 2
        
        # Test page 2
        response = client.get("/api/products?page=2&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5, "Should return 5 remaining items on page 2"
        assert data["page"] == 2

    def test_product_search_by_category(self, client, test_db, sample_category):
        """Verify category filtering works for frontend product catalog."""
        from app.models.product import Product
        from app.models.category import Category
        
        # Create second category
        category2 = Category(
            name="Category 2",
            description="Second test category"
        )
        test_db.add(category2)
        test_db.commit()
        test_db.refresh(category2)
        
        # Create products in different categories
        for i in range(3):
            product = Product(
                name=f"Product Cat1-{i}",
                description=f"Description {i}",
                brand="TestBrand",
                sku=f"CAT1-{i:03d}",
                price=10.0 + i,
                category_id=sample_category.id,
                is_active="active",
            )
            test_db.add(product)
        
        for i in range(2):
            product = Product(
                name=f"Product Cat2-{i}",
                description=f"Description {i}",
                brand="TestBrand",
                sku=f"CAT2-{i:03d}",
                price=20.0 + i,
                category_id=category2.id,
                is_active="active",
            )
            test_db.add(product)
        test_db.commit()
        
        # Test filtering by category
        response = client.get(f"/api/products?category_id={sample_category.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 3, "Should return only products from category 1"
        assert all(p["category_id"] == sample_category.id for p in data["items"])


class TestCartIntegration:
    """Integration tests for Shopping Cart API."""

    def test_get_cart_api_contract(self, client):
        """Verify GET /api/cart response includes all required fields."""
        response = client.get("/api/cart")
        
        assert response.status_code == status.HTTP_200_OK
        cart = response.json()
        
        # Verify cart structure
        assert "id" in cart
        assert "customer_id" in cart
        assert "items" in cart
        assert "total_items" in cart
        assert "subtotal" in cart

    def test_cart_api_endpoint_exists(self, client):
        """Verify cart API endpoint is accessible."""
        # Just verify the endpoint exists and returns valid structure
        response = client.get("/api/cart")
        assert response.status_code == status.HTTP_200_OK
        
        cart = response.json()
        # Verify basic cart structure
        assert "items" in cart
        assert "total_items" in cart


class TestAuthenticationIntegration:
    """Integration tests for Authentication API."""

    def test_register_api_contract(self, client):
        """Verify POST /api/auth/register response matches frontend expectations."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Verify response structure
        assert "access_token" in data, "Registration should return access_token"
        assert "token_type" in data, "Registration should return token_type"
        assert "user" in data, "Registration should return user object"
        assert data["token_type"] == "bearer"
        
        # Verify user object
        user = data["user"]
        assert "id" in user
        assert "email" in user
        assert "full_name" in user
        assert user["email"] == "newuser@example.com"

    def test_login_api_contract(self, client, sample_customer):
        """Verify POST /api/auth/login response matches frontend expectations."""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "TestPassword123!"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure
        assert "access_token" in data, "Login should return access_token"
        assert "token_type" in data, "Login should return token_type"
        assert "user" in data, "Login should return user object"
        assert isinstance(data["access_token"], str), "Access token should be string"
        assert len(data["access_token"]) > 0, "Access token should not be empty"
        assert data["token_type"] == "bearer"


class TestOrderProcessingIntegration:
    """Integration tests for Order Processing API."""

    def test_orders_api_endpoint_exists(self, client):
        """Verify orders API endpoint exists."""
        # Orders endpoint should require auth, so 401 or 422 is expected
        response = client.get("/api/orders")
        
        # Should not be 404 - endpoint should exist
        assert response.status_code != 404, "Orders endpoint should exist"


class TestDiscountIntegration:
    """Integration tests for Discount/Promotion API."""

    def test_list_discounts_api_contract(self, client):
        """Verify GET /api/discounts response structure."""
        response = client.get("/api/discounts")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response is list or paginated structure
        assert isinstance(data, (list, dict))


class TestErrorHandling:
    """Test error response formats match frontend expectations."""

    def test_404_error_format(self, client):
        """Verify 404 errors return consistent format."""
        response = client.get("/api/products/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data, "Error response should include 'detail' field"

    def test_validation_error_format(self, client):
        """Verify validation errors return consistent format."""
        # Try to add invalid product to cart
        response = client.post(
            "/api/cart/items",
            json={"product_id": 99999, "quantity": 1}
        )
        
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
        data = response.json()
        assert "detail" in data


class TestAPIAvailability:
    """Test that all critical API endpoints are available."""

    def test_products_endpoint_available(self, client):
        """Verify /api/products endpoint is available."""
        response = client.get("/api/products")
        assert response.status_code == status.HTTP_200_OK

    def test_cart_endpoint_available(self, client):
        """Verify /api/cart endpoint is available."""
        response = client.get("/api/cart")
        assert response.status_code == status.HTTP_200_OK

    def test_auth_register_endpoint_available(self, client):
        """Verify /api/auth/register endpoint is available."""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "short", "full_name": "Test"}
        )
        # Should return 400 for validation error, not 404
        assert response.status_code != status.HTTP_404_NOT_FOUND

    def test_discounts_endpoint_available(self, client):
        """Verify /api/discounts endpoint is available."""
        response = client.get("/api/discounts")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]

    def test_categories_endpoint_available(self, client):
        """Verify /api/categories endpoint is available."""
        response = client.get("/api/categories")
        # Should return 200 or another valid status, not 404
        assert response.status_code != status.HTTP_404_NOT_FOUND
