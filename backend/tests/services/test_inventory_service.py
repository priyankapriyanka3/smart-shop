"""Tests for inventory service."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.product import Product
from app.models.category import Category
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.services import inventory_service

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_inventory_service.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Setup and teardown test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create a test database session."""
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_inventory_record(db_session):
    """Create test inventory record with dependencies."""
    # Create category
    category = Category(name="Electronics", description="Electronic items", is_active=True)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    # Create product
    product = Product(
        name="Test Product",
        description="A test product",
        brand="TestBrand",
        sku="TEST001",
        price=99.99,
        category_id=category.id,
        is_active="active",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    
    # Create warehouse
    warehouse = Warehouse(name="Main Warehouse", location="Location A")
    db_session.add(warehouse)
    db_session.commit()
    db_session.refresh(warehouse)
    
    # Create inventory record
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity=50,
        reorder_level=10,
    )
    db_session.add(inventory)
    db_session.commit()
    db_session.refresh(inventory)
    
    return inventory


@pytest.fixture
def test_actor(db_session):
    """Create test actor for audit logging."""
    customer = Customer(
        email="admin@example.com",
        password_hash="hashed",
        full_name="Admin User",
        role="admin",
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


def test_get_inventory_records(db_session, test_inventory_record):
    """Test getting paginated inventory records."""
    records, total = inventory_service.get_inventory_records(db_session, page=1, per_page=20)
    assert total >= 1
    assert len(records) >= 1
    assert records[0].product_name == "Test Product"
    assert records[0].warehouse_name == "Main Warehouse"


def test_get_inventory_by_id(db_session, test_inventory_record):
    """Test getting inventory by ID."""
    inventory = inventory_service.get_inventory_by_id(db_session, test_inventory_record.id)
    assert inventory is not None
    assert inventory.id == test_inventory_record.id
    assert inventory.quantity == 50


def test_update_inventory_quantity(db_session, test_inventory_record, test_actor):
    """Test updating inventory quantity."""
    updated = inventory_service.update_inventory_quantity(
        db_session, test_inventory_record.id, 100, test_actor.id
    )
    assert updated is not None
    assert updated.quantity == 100


def test_get_low_stock_items(db_session, test_inventory_record):
    """Test getting low stock items."""
    # Update inventory to be below reorder level
    test_inventory_record.quantity = 5
    db_session.commit()
    
    low_stock = inventory_service.get_low_stock_items(db_session)
    assert len(low_stock) >= 1
    assert low_stock[0]["current_quantity"] == 5
    assert low_stock[0]["reorder_level"] == 10


def test_update_inventory_not_found(db_session, test_actor):
    """Test updating non-existent inventory record."""
    updated = inventory_service.update_inventory_quantity(db_session, 99999, 100, test_actor.id)
    assert updated is None
