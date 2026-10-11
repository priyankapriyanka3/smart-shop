"""
Acceptance tests for seed data script.

Verifies REQ-DATA-002: Seed Data with Default Credentials and Sample Records
"""
import pytest
from sqlalchemy import create_engine, text
import bcrypt
import os
from app.database import Base
from app.seed import seed_database
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def test_db():
    """Create a test database for seed testing."""
    # Use in-memory SQLite for testing
    test_database_url = "sqlite:///:memory:"
    engine = create_engine(test_database_url)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()
    
    yield db_session, engine
    
    db_session.close()


def test_admin_user_seeded(test_db):
    """Verify admin@example.com user created with bcrypt-hashed password for admin123."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        admin = conn.execute(
            text('SELECT email, password_hash, status FROM users WHERE email = :email'),
            {"email": "admin@example.com"}
        ).fetchone()
        
        assert admin is not None, "Admin user should exist"
        assert admin[0] == "admin@example.com"
        assert admin[2] == "active"
        
        # Verify bcrypt with cost factor 12
        password_hash = admin[1]
        assert password_hash.startswith("$2b$12$"), "Password should use bcrypt with cost factor 12"
        
        # Verify password
        assert bcrypt.checkpw(b"admin123", password_hash.encode("utf-8")), "Password should verify"


def test_admin_role_assigned(test_db):
    """Verify admin user assigned admin role."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        admin_role = conn.execute(
            text('''
                SELECT r.name 
                FROM users u 
                JOIN user_roles ur ON u.id = ur.user_id 
                JOIN roles r ON ur.role_id = r.id 
                WHERE u.email = :email
            '''),
            {"email": "admin@example.com"}
        ).fetchone()
        
        assert admin_role is not None, "Admin should have a role"
        assert admin_role[0] == "admin", "Admin should have admin role"


def test_all_roles_seeded(test_db):
    """Verify all roles (admin, inventory_manager, customer_support, customer) seeded."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        roles = conn.execute(text('SELECT name FROM roles ORDER BY name')).fetchall()
        role_names = [r[0] for r in roles]
        
        required_roles = ['admin', 'customer', 'customer_support', 'inventory_manager']
        for role in required_roles:
            assert role in role_names, f"Role {role} should exist"


def test_role_permissions_mapping(test_db):
    """Verify ROLE_PERMISSIONS map includes all seeded roles."""
    from app.auth.rbac import ROLE_PERMISSIONS
    
    required_roles = ['admin', 'customer', 'customer_support', 'inventory_manager']
    for role in required_roles:
        assert role in ROLE_PERMISSIONS, f"Role {role} should be in ROLE_PERMISSIONS"
        assert len(ROLE_PERMISSIONS[role]) > 0, f"Role {role} should have permissions"


def test_products_seeded(test_db):
    """Verify at least 100 products seeded across at least 50 categories."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        product_count = conn.execute(
            text('SELECT COUNT(*) FROM products WHERE status = :status'),
            {"status": "active"}
        ).scalar()
        
        category_count = conn.execute(
            text('SELECT COUNT(*) FROM categories WHERE status = :status'),
            {"status": "active"}
        ).scalar()
        
        assert product_count >= 100, f"Should have at least 100 products, got {product_count}"
        assert category_count >= 50, f"Should have at least 50 categories, got {category_count}"


def test_warehouses_suppliers_seeded(test_db):
    """Verify warehouses, suppliers, inventory records seeded."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        warehouse_count = conn.execute(text('SELECT COUNT(*) FROM warehouses')).scalar()
        supplier_count = conn.execute(text('SELECT COUNT(*) FROM suppliers')).scalar()
        inventory_count = conn.execute(text('SELECT COUNT(*) FROM inventory')).scalar()
        
        assert 3 <= warehouse_count <= 5, f"Should have 3-5 warehouses, got {warehouse_count}"
        assert 10 <= supplier_count <= 20, f"Should have 10-20 suppliers, got {supplier_count}"
        assert inventory_count > 0, "Should have inventory records"


def test_promotions_seeded(test_db):
    """Verify sample promotions with valid date ranges and usage limits."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        promo_count = conn.execute(text('SELECT COUNT(*) FROM promotions')).scalar()
        assert promo_count > 0, "Should have promotions"
        
        # Check a sample promotion
        promo = conn.execute(
            text('SELECT code, start_date, end_date, max_uses FROM promotions LIMIT 1')
        ).fetchone()
        
        assert promo is not None, "Should have at least one promotion"
        assert promo[1] is not None, "Promotion should have start_date"
        assert promo[2] is not None, "Promotion should have end_date"
        assert promo[3] is not None, "Promotion should have max_uses"


def test_reviews_seeded(test_db):
    """Verify sample reviews linked to products and customers."""
    db_session, engine = test_db
    seed_database(db_session)
    
    with engine.connect() as conn:
        review_count = conn.execute(text('SELECT COUNT(*) FROM reviews')).scalar()
        assert review_count > 0, "Should have reviews"
        
        # Verify review linkage
        linked_review = conn.execute(
            text('''
                SELECT r.id, r.product_id, r.customer_id 
                FROM reviews r 
                JOIN products p ON r.product_id = p.id 
                JOIN users u ON r.customer_id = u.id 
                LIMIT 1
            ''')
        ).fetchone()
        
        assert linked_review is not None, "Reviews should be linked to products and customers"


def test_seed_idempotent(test_db):
    """Verify seed script idempotent: running twice does not create duplicates."""
    db_session, engine = test_db
    
    # Run seed first time
    seed_database(db_session)
    
    with engine.connect() as conn:
        first_product_count = conn.execute(text('SELECT COUNT(*) FROM products')).scalar()
        first_user_count = conn.execute(text('SELECT COUNT(*) FROM users')).scalar()
    
    # Run seed second time
    seed_database(db_session)
    
    with engine.connect() as conn:
        second_product_count = conn.execute(text('SELECT COUNT(*) FROM products')).scalar()
        second_user_count = conn.execute(text('SELECT COUNT(*) FROM users')).scalar()
    
    assert first_product_count == second_product_count, "Product count should not change"
    assert first_user_count == second_user_count, "User count should not change"
