"""Test configuration and fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Import all models to ensure they are registered with Base
from app.models import (  # noqa: F401
    audit_log,
    cart,
    cart_item,
    category,
    customer,
    discount,
    inventory,
    order,
    order_item,
    product,
    review,
    supplier,
    warehouse,
)

from app.models.category import Category
from app.models.customer import Customer
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory


# Use in-memory SQLite for tests with shared cache
# Note: Using ?mode=memory&cache=shared to ensure all connections share the same in-memory database
TEST_DATABASE_URL = "sqlite:///file:test_db?mode=memory&cache=shared&uri=true"


@pytest.fixture(scope="function")
def test_db():
    """Create test database session with all tables."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with overridden database dependency."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_category(test_db):
    """Create sample category."""
    category = Category(
        name="Electronics",
        description="Electronic devices and accessories",
        is_active=True,
    )
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    return category


@pytest.fixture(scope="function")
def sample_product(test_db, sample_category):
    """Create sample product."""
    product = Product(
        name="Test Product",
        description="A test product description",
        brand="TestBrand",
        sku="TEST-001",
        price=99.99,
        category_id=sample_category.id,
        is_active="active",
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    return product


@pytest.fixture(scope="function")
def sample_customer(test_db):
    """Create sample customer with properly hashed password."""
    from app.auth.password import hash_password
    
    customer = Customer(
        email="test@example.com",
        password_hash=hash_password("TestPassword123!"),
        full_name="Test User",
        role="shopper",
        is_active=True,
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    return customer


@pytest.fixture(scope="function")
def sample_warehouse(test_db):
    """Create sample warehouse."""
    warehouse = Warehouse(
        name="Main Warehouse",
        location="Test Location",
    )
    test_db.add(warehouse)
    test_db.commit()
    test_db.refresh(warehouse)
    return warehouse


@pytest.fixture(scope="function")
def sample_inventory(test_db, sample_product, sample_warehouse):
    """Create sample inventory."""
    inventory = Inventory(
        product_id=sample_product.id,
        warehouse_id=sample_warehouse.id,
        quantity=100,
        reorder_level=10,
    )
    test_db.add(inventory)
    test_db.commit()
    test_db.refresh(inventory)
    return inventory


@pytest.fixture(scope="function")
def auth_headers(sample_customer):
    """Create authentication headers for test requests."""
    from app.auth.jwt import create_access_token
    
    token = create_access_token(sample_customer.id, sample_customer.role)
    return {"Authorization": f"Bearer {token}"}
