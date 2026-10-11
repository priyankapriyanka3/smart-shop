"""Test fixtures and configuration for backend tests."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Clear DATABASE_URL from host environment and set TESTING=1 BEFORE any app imports
# The host may have a postgresql+asyncpg URL that would require asyncpg driver
if "DATABASE_URL" in os.environ:
    del os.environ["DATABASE_URL"]
os.environ["TESTING"] = "1"

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models import *  # Import all models
from app.auth.password import hash_password
from datetime import datetime, timedelta


# Test database setup
# Use a named shared-memory database so all connections see the same data
# Each :memory: URL creates a separate database, but file::memory:?cache=shared
# creates a shared database accessible from all connections in the same process
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use StaticPool to ensure single connection is reused
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create test database and provide session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with overridden database dependency."""
    # TESTING=1 is set at module level to disable seeding and rate limiting
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create a test customer user."""
    from app.models.customers import User
    from app.models.admin import Role, UserRole
    
    # Create customer role
    customer_role = Role(name="customer", description="Customer role")
    db.add(customer_role)
    db.commit()
    
    # Create user
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("testpass123"),
        status="active",
        is_deleted=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assign customer role
    user_role = UserRole(user_id=user.id, role_id=customer_role.id)
    db.add(user_role)
    db.commit()
    
    return user


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    from app.models.customers import User
    from app.models.admin import Role, UserRole
    
    # Create admin role
    admin_role = Role(name="admin", description="Admin role")
    db.add(admin_role)
    db.commit()
    
    # Create user
    user = User(
        email="admin@test.com",
        name="Admin User",
        password_hash=hash_password("adminpass123"),
        status="active",
        is_deleted=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assign admin role
    user_role = UserRole(user_id=user.id, role_id=admin_role.id)
    db.add(user_role)
    db.commit()
    
    return user


@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client, admin_user):
    """Get authentication token for admin user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "adminpass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def test_category(db):
    """Create a test category."""
    from app.models.catalog import Category
    
    category = Category(
        name="Test Category",
        slug="test-category",
        description="Test category description",
        status="active",
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture
def test_product(db, test_category):
    """Create a test product."""
    from app.models.catalog import Product
    
    product = Product(
        name="Test Product",
        slug="test-product",
        sku="TEST-001",
        description="Test product description",
        price=99.99,
        brand="Test Brand",
        category_id=test_category.id,
        image_url="https://example.com/test.jpg",
        status="active",
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture
def test_warehouse(db):
    """Create a test warehouse."""
    from app.models.inventory import Warehouse
    
    warehouse = Warehouse(
        name="Test Warehouse",
        code="TEST-WH-001",
        location="Test Location",
        status="active",
    )
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@pytest.fixture
def test_inventory(db, test_product, test_warehouse):
    """Create test inventory."""
    from app.models.inventory import Inventory
    
    inventory = Inventory(
        product_id=test_product.id,
        warehouse_id=test_warehouse.id,
        quantity=100,
        reorder_level=20,
        status="in_stock",
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


@pytest.fixture
def test_promotion(db):
    """Create a test promotion."""
    from app.models.promotions import Promotion
    
    now = datetime.utcnow()
    promotion = Promotion(
        name="Test Promotion",
        code="TEST10",
        discount_type="percentage",
        discount_value=10.0,
        minimum_order_amount=50.0,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(days=30),
        max_uses=100,
        current_uses=0,
        status="active",
    )
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


@pytest.fixture
def expired_promotion(db):
    """Create an expired promotion."""
    from app.models.promotions import Promotion
    
    now = datetime.utcnow()
    promotion = Promotion(
        name="Expired Promotion",
        code="EXPIRED",
        discount_type="percentage",
        discount_value=20.0,
        minimum_order_amount=0.0,
        start_date=now - timedelta(days=30),
        end_date=now - timedelta(days=1),
        max_uses=100,
        current_uses=0,
        status="active",
    )
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


@pytest.fixture
def test_order(db, test_user, test_product):
    """Create a test order."""
    from app.models.orders import Order, OrderItem
    
    order = Order(
        customer_id=test_user.id,
        order_number="ORD-TEST-001",
        status="placed",
        subtotal=99.99,
        discount_amount=0.0,
        shipping_cost=10.0,
        total=109.99,
        shipping_street="123 Test St",
        shipping_city="Test City",
        shipping_state_province="Test State",
        shipping_postal_code="12345",
        shipping_country="Test Country",
        billing_street="123 Test St",
        billing_city="Test City",
        billing_state_province="Test State",
        billing_postal_code="12345",
        billing_country="Test Country",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Add order item
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=1,
        unit_price=99.99,
        total_price=99.99,
    )
    db.add(order_item)
    db.commit()
    
    return order


@pytest.fixture
def test_review(db, test_user, test_product):
    """Create a test review."""
    from app.models.reviews import Review
    
    review = Review(
        product_id=test_product.id,
        customer_id=test_user.id,
        rating=5,
        title="Great product",
        review_text="This product is excellent!",
        status="pending",
        helpful_count=0,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@pytest.fixture
def test_user_with_address(db):
    """Create a test user with address."""
    from app.models.customers import User, Address
    from app.models.admin import Role, UserRole
    
    # Create customer role
    customer_role = db.query(Role).filter(Role.name == "customer").first()
    if not customer_role:
        customer_role = Role(name="customer", description="Customer role")
        db.add(customer_role)
        db.commit()
    
    # Create user
    user = User(
        email="user_with_addr@example.com",
        name="User With Address",
        password_hash=hash_password("testpass123"),
        status="active",
        is_deleted=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assign customer role
    user_role = UserRole(user_id=user.id, role_id=customer_role.id)
    db.add(user_role)
    
    # Create address
    address = Address(
        user_id=user.id,
        address_type="shipping",
        street="456 Test Avenue",
        city="Test City",
        state_province="Test State",
        postal_code="54321",
        country="Test Country",
        is_default=True,
    )
    db.add(address)
    db.commit()
    db.refresh(user)
    
    return user
