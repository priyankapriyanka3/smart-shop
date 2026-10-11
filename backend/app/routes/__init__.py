"""Route package exports."""

from app.routes.cart import router as cart_router
from app.routes.categories import router as categories_router
from app.routes.discounts import router as discounts_router
from app.routes.inventory import router as inventory_router
from app.routes.orders import router as orders_router
from app.routes.products import router as products_router
from app.routes.reviews import router as reviews_router
from app.routes.search import router as search_router
from app.routes.suppliers import router as suppliers_router

__all__ = [
    "cart_router",
    "categories_router",
    "discounts_router",
    "inventory_router",
    "orders_router",
    "products_router",
    "reviews_router",
    "search_router",
    "suppliers_router",
]
