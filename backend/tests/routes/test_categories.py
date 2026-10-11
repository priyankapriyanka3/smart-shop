"""Tests for category routes."""
from fastapi import status


def test_list_categories_empty(client):
    """Test listing categories with empty database."""
    response = client.get("/api/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_categories_with_data(client, sample_category):
    """Test listing categories with sample data."""
    response = client.get("/api/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Electronics"
    assert data[0]["is_active"] is True
    assert "subcategories" in data[0]


def test_list_categories_hierarchy(client, test_db):
    """Test category hierarchy with parent-child relationships."""
    from app.models.category import Category

    # Create parent category
    parent = Category(
        name="Electronics",
        description="Electronic devices",
        is_active=True,
    )
    test_db.add(parent)
    test_db.commit()
    test_db.refresh(parent)

    # Create child categories
    child1 = Category(
        name="Mobile Phones",
        description="Smartphones and accessories",
        parent_id=parent.id,
        is_active=True,
    )
    child2 = Category(
        name="Laptops",
        description="Laptop computers",
        parent_id=parent.id,
        is_active=True,
    )
    test_db.add_all([child1, child2])
    test_db.commit()

    response = client.get("/api/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should return only root categories with nested subcategories
    assert len(data) == 1
    assert data[0]["name"] == "Electronics"
    assert len(data[0]["subcategories"]) == 2
    
    subcategory_names = {sub["name"] for sub in data[0]["subcategories"]}
    assert "Mobile Phones" in subcategory_names
    assert "Laptops" in subcategory_names


def test_get_category_by_id(client, sample_category):
    """Test getting category by ID."""
    response = client.get(f"/api/categories/{sample_category.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_category.id
    assert data["name"] == "Electronics"
    assert data["description"] == "Electronic devices and accessories"
    assert data["is_active"] is True
    assert "created_at" in data
    assert "updated_at" in data


def test_get_category_not_found(client):
    """Test getting non-existent category."""
    response = client.get("/api/categories/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_list_category_products_empty(client, sample_category):
    """Test listing products in category with no products."""
    response = client.get(f"/api/categories/{sample_category.id}/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


def test_list_category_products_with_data(client, sample_product, sample_inventory):
    """Test listing products in category with sample data."""
    response = client.get(f"/api/categories/{sample_product.category_id}/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Test Product"
    assert data["items"][0]["category_id"] == sample_product.category_id
    assert data["items"][0]["stock_status"] == "in_stock"


def test_list_category_products_pagination(client, test_db, sample_category):
    """Test category products pagination."""
    from app.models.product import Product

    # Create multiple products in the same category
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
    response = client.get(f"/api/categories/{sample_category.id}/products?page=1&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["pages"] == 3
    assert data["page"] == 1

    # Test page 2
    response = client.get(f"/api/categories/{sample_category.id}/products?page=2&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 2


def test_list_category_products_not_found(client):
    """Test listing products for non-existent category."""
    response = client.get("/api/categories/999/products")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_list_category_products_only_active(client, test_db, sample_category):
    """Test that only active products are returned."""
    from app.models.product import Product

    # Create active and inactive products
    active_product = Product(
        name="Active Product",
        description="Active product",
        brand="TestBrand",
        sku="ACTIVE-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="active",
    )
    inactive_product = Product(
        name="Inactive Product",
        description="Inactive product",
        brand="TestBrand",
        sku="INACTIVE-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="inactive",
    )
    draft_product = Product(
        name="Draft Product",
        description="Draft product",
        brand="TestBrand",
        sku="DRAFT-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="draft",
    )
    test_db.add_all([active_product, inactive_product, draft_product])
    test_db.commit()

    response = client.get(f"/api/categories/{sample_category.id}/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should only return active products
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Active Product"
    assert data["items"][0]["is_active"] == "active"


def test_category_with_subcategories_structure(client, test_db):
    """Test deeply nested category hierarchy."""
    from app.models.category import Category

    # Create root
    root = Category(name="Root", description="Root category", is_active=True)
    test_db.add(root)
    test_db.commit()
    test_db.refresh(root)

    # Create level 1 child
    level1 = Category(
        name="Level 1",
        description="Level 1 category",
        parent_id=root.id,
        is_active=True,
    )
    test_db.add(level1)
    test_db.commit()
    test_db.refresh(level1)

    # Create level 2 children
    level2a = Category(
        name="Level 2A",
        description="Level 2A category",
        parent_id=level1.id,
        is_active=True,
    )
    level2b = Category(
        name="Level 2B",
        description="Level 2B category",
        parent_id=level1.id,
        is_active=True,
    )
    test_db.add_all([level2a, level2b])
    test_db.commit()

    response = client.get("/api/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify root level
    assert len(data) == 1
    assert data[0]["name"] == "Root"
    
    # Verify level 1
    assert len(data[0]["subcategories"]) == 1
    assert data[0]["subcategories"][0]["name"] == "Level 1"
    
    # Verify level 2
    level1_data = data[0]["subcategories"][0]
    assert len(level1_data["subcategories"]) == 2
    level2_names = {sub["name"] for sub in level1_data["subcategories"]}
    assert "Level 2A" in level2_names
    assert "Level 2B" in level2_names


def test_get_category_with_parent(client, test_db):
    """Test getting category that has a parent."""
    from app.models.category import Category

    # Create parent
    parent = Category(name="Parent", description="Parent category", is_active=True)
    test_db.add(parent)
    test_db.commit()
    test_db.refresh(parent)

    # Create child
    child = Category(
        name="Child",
        description="Child category",
        parent_id=parent.id,
        is_active=True,
    )
    test_db.add(child)
    test_db.commit()
    test_db.refresh(child)

    response = client.get(f"/api/categories/{child.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Child"
    assert data["parent_id"] == parent.id
