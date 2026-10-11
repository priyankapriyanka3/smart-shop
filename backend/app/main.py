"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import (
    cart_router,
    categories_router,
    discounts_router,
    inventory_router,
    orders_router,
    products_router,
    reviews_router,
    search_router,
    suppliers_router,
)
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup: database initialization happens here in later tasks
    yield
    # Shutdown: cleanup happens here


app = FastAPI(
    title="Smart Shop API",
    description="E-commerce platform API for Smart Shop",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(products_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(orders_router, prefix="/api/orders", tags=["orders"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["inventory"])
app.include_router(discounts_router, prefix="/api/discounts", tags=["discounts"])
app.include_router(reviews_router, prefix="/api", tags=["reviews"])
app.include_router(suppliers_router, prefix="/api/suppliers", tags=["suppliers"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "smart-shop-api"}
