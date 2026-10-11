"""Test configuration and fixtures."""
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Disable OpenTelemetry for tests to prevent connection attempts and hangs
os.environ["OTEL_SDK_DISABLED"] = "true"

# Import all models to ensure they are registered with Base
import app.models.audit_log  # noqa: F401
import app.models.cart  # noqa: F401
import app.models.cart_item  # noqa: F401
import app.models.category  # noqa: F401
import app.models.customer  # noqa: F401
import app.models.discount  # noqa: F401
import app.models.inventory  # noqa: F401
import app.models.order  # noqa: F401
import app.models.order_item  # noqa: F401
import app.models.product  # noqa: F401
import app.models.review  # noqa: F401
import app.models.supplier  # noqa: F401
import app.models.warehouse  # noqa: F401
from app.database import Base, get_db
from app.main import app
from app.models.category import Category
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine with shared in-memory database."""
    # Use StaticPool to ensure all connections share the same in-memory database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Critical: shares one connection across all sessions
    )

    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session with all tables."""
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = testing_session_local()

    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def client(test_engine):
    """Create test client with overridden database dependency."""
    # Create a session factory bound to the test engine
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        """Override get_db to return test database session."""
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

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
