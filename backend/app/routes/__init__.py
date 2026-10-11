"""Route modules for Smart Shop API."""
from app.routes import (
    auth,
    catalog,
    customers,
    cart,
    checkout,
    orders,
    payments,
    inventory,
    promotions,
    reviews,
    admin,
)

__all__ = [
    "auth",
    "catalog",
    "customers",
    "cart",
    "checkout",
    "orders",
    "payments",
    "inventory",
    "promotions",
    "reviews",
    "admin",
]
