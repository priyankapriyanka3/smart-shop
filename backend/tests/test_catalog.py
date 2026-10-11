"""Catalog domain tests."""
import pytest
from fastapi import status


class TestProductList:
    """Test product listing endpoints."""
    
    def test_get_products_list(self, client, test_product, test_inventory):
        """Test getting product list."""
        response = client.get("/api/v1/catalog/products")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert data["total"] >= 1
        
        # Check product structure
        product = data["items"][0]
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "sku" in product
    
    def test_get_products_with_pagination(self, client, db, test_category):
        """Test product list pagination."""
        from app.models.catalog import Product
        
        # Create multiple products
        for i in range(25):
            product = Product(
                name=f"Product {i}",
                slug=f"product-{i}",
                sku=f"SKU-{i:03d}",
                price=10.0 + i,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        # Get first page
        response = client.get("/api/v1/catalog/products?page=1&page_size=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 1
        assert data["total"] >= 25
        
        # Get second page
        response = client.get("/api/v1/catalog/products?page=2&page_size=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 2


class TestProductDetail:
    """Test product detail endpoint."""
    
    def test_get_product_by_id(self, client, test_product, test_inventory):
        """Test getting product by ID."""
        response = client.get(f"/api/v1/catalog/products/{test_product.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_product.id
        assert data["name"] == test_product.name
        assert data["sku"] == test_product.sku
        assert data["price"] == test_product.price
        assert "available_quantity" in data
        assert data["available_quantity"] == 100
    
    def test_get_product_not_found(self, client):
        """Test getting non-existent product."""
        response = client.get("/api/v1/catalog/products/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestProductSearch:
    """Test product search functionality."""
    
    def test_search_by_keyword(self, client, db, test_category):
        """Test searching products by keyword."""
        from app.models.catalog import Product
        
        # Create products with different names
        products_data = [
            ("Laptop Computer", "laptop-computer", "LAPTOP-001"),
            ("Desktop Computer", "desktop-computer", "DESKTOP-001"),
            ("Wireless Mouse", "wireless-mouse", "MOUSE-001"),
        ]
        
        for name, slug, sku in products_data:
            product = Product(
                name=name,
                slug=slug,
                sku=sku,
                price=99.99,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        # Search for "computer"
        response = client.get("/api/v1/catalog/search?q=computer")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        
        # All results should contain "computer"
        for item in data["items"]:
            assert "computer" in item["name"].lower()
    
    def test_search_by_sku(self, client, test_product):
        """Test searching products by SKU."""
        response = client.get(f"/api/v1/catalog/search?q={test_product.sku}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] >= 1
        assert any(item["sku"] == test_product.sku for item in data["items"])
    
    def test_search_no_results(self, client):
        """Test search with no matching results."""
        response = client.get("/api/v1/catalog/search?q=nonexistentproduct12345")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0


class TestCategoryFilter:
    """Test product filtering by category."""
    
    def test_filter_by_category(self, client, db, test_category):
        """Test filtering products by category."""
        from app.models.catalog import Product, Category
        
        # Create another category
        other_category = Category(
            name="Other Category",
            slug="other-category",
            status="active",
        )
        db.add(other_category)
        db.commit()
        
        # Create products in both categories
        for i in range(3):
            product = Product(
                name=f"Test Product {i}",
                slug=f"test-product-{i}",
                sku=f"TEST-{i:03d}",
                price=50.0,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        
        for i in range(2):
            product = Product(
                name=f"Other Product {i}",
                slug=f"other-product-{i}",
                sku=f"OTHER-{i:03d}",
                price=75.0,
                brand="Test Brand",
                category_id=other_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        # Filter by test_category
        response = client.get(f"/api/v1/catalog/products?category_id={test_category.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 3
        
        # Filter by other_category
        response = client.get(f"/api/v1/catalog/products?category_id={other_category.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2


class TestProductFilters:
    """Test advanced product filtering."""
    
    def test_filter_by_price_range(self, client, db, test_category):
        """Test filtering products by price range."""
        from app.models.catalog import Product
        
        # Create products with different prices
        prices = [25.0, 50.0, 75.0, 100.0, 150.0]
        for i, price in enumerate(prices):
            product = Product(
                name=f"Product {i}",
                slug=f"product-{i}",
                sku=f"PRICE-{i:03d}",
                price=price,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        # Filter by price range 50-100
        response = client.get("/api/v1/catalog/products?min_price=50&max_price=100")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should get products with prices 50, 75, 100
        assert data["total"] == 3
        for item in data["items"]:
            assert 50.0 <= item["price"] <= 100.0
    
    def test_filter_by_brand(self, client, db, test_category):
        """Test filtering products by brand."""
        from app.models.catalog import Product
        
        # Create products with different brands
        brands = ["Brand A", "Brand B", "Brand A"]
        for i, brand in enumerate(brands):
            product = Product(
                name=f"Product {i}",
                slug=f"brand-product-{i}",
                sku=f"BRAND-{i:03d}",
                price=50.0,
                brand=brand,
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        # Filter by Brand A
        response = client.get("/api/v1/catalog/products?brand=Brand A")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        
        for item in data["items"]:
            assert item["brand"] == "Brand A"


class TestProductSorting:
    """Test product sorting."""
    
    def test_sort_by_price_ascending(self, client, db, test_category):
        """Test sorting products by price (low to high)."""
        from app.models.catalog import Product
        
        # Create products with different prices
        prices = [100.0, 25.0, 75.0, 50.0]
        for i, price in enumerate(prices):
            product = Product(
                name=f"Product {i}",
                slug=f"sort-product-{i}",
                sku=f"SORT-{i:03d}",
                price=price,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        response = client.get("/api/v1/catalog/products?sort_by=price_asc")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Prices should be in ascending order
        prices_result = [item["price"] for item in data["items"]]
        assert prices_result == sorted(prices_result)
    
    def test_sort_by_price_descending(self, client, db, test_category):
        """Test sorting products by price (high to low)."""
        from app.models.catalog import Product
        
        # Create products with different prices
        prices = [50.0, 100.0, 25.0, 75.0]
        for i, price in enumerate(prices):
            product = Product(
                name=f"Product {i}",
                slug=f"sort-desc-{i}",
                sku=f"SORTD-{i:03d}",
                price=price,
                brand="Test Brand",
                category_id=test_category.id,
                status="active",
            )
            db.add(product)
        db.commit()
        
        response = client.get("/api/v1/catalog/products?sort_by=price_desc")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Prices should be in descending order
        prices_result = [item["price"] for item in data["items"]]
        assert prices_result == sorted(prices_result, reverse=True)


class TestCategoryEndpoints:
    """Test category endpoints."""
    
    def test_get_categories_list(self, client, test_category):
        """Test getting categories list."""
        response = client.get("/api/v1/catalog/categories")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1
        
        # Check category structure
        category = data["items"][0]
        assert "id" in category
        assert "name" in category
        assert "slug" in category
    
    def test_get_category_by_id(self, client, test_category):
        """Test getting category by ID."""
        response = client.get(f"/api/v1/catalog/categories/{test_category.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_category.id
        assert data["name"] == test_category.name
        assert data["slug"] == test_category.slug
