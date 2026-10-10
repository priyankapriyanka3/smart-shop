"""Database configuration and session management."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Get DATABASE_URL from environment, default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Configure connect_args for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Set to True for SQL logging during development
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """Dependency for FastAPI routes to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables."""
    # Import all models here to ensure they are registered with Base
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

    Base.metadata.create_all(bind=engine)
