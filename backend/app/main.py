"""Smart Shop FastAPI main application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import Base, engine
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Runs database initialization and seed data on startup.
    """
    import os
    
    # Skip database setup during tests (tests manage their own database)
    if os.getenv("TESTING") == "1":
        yield
        return
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Run seed data
    try:
        from app.seed import seed_database
        from app.dependencies import get_db
        
        # Create a session and run seeding
        db_session = next(get_db())
        try:
            seed_database(db_session)
        finally:
            db_session.close()
    except ImportError:
        print("Info: Seed module not yet available")
    except Exception as e:
        print(f"Warning: Seed data failed: {e}")
    
    yield
    
    # Cleanup (if needed)
    pass


# Create FastAPI application
app = FastAPI(
    title="Smart Shop API",
    description="E-commerce platform API for Smart Shop",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware (REQ-SEC-001)
app.add_middleware(SecurityHeadersMiddleware)

# Add rate limiting middleware for authentication endpoints
# 5 attempts per email per 15 minutes (REQ-API-003)
app.add_middleware(RateLimitMiddleware, max_attempts=5, window_minutes=15)


# Global exception handler for standard error format
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all exceptions with standard error format."""
    if hasattr(exc, "status_code"):
        status_code = exc.status_code
        detail = str(exc.detail) if hasattr(exc, "detail") else str(exc)
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = "Internal server error"
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail, "status_code": status_code},
    )


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "name": "Smart Shop API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers with /api/v1 prefix
api_prefix = settings.api_base_path

app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(catalog.router, prefix=f"{api_prefix}/catalog", tags=["Catalog"])
app.include_router(customers.router, prefix=f"{api_prefix}/customers", tags=["Customers"])
app.include_router(cart.router, prefix=f"{api_prefix}/cart", tags=["Cart"])
app.include_router(checkout.router, prefix=f"{api_prefix}/checkout", tags=["Checkout"])
app.include_router(orders.router, prefix=f"{api_prefix}/orders", tags=["Orders"])
app.include_router(payments.router, prefix=f"{api_prefix}/payments", tags=["Payments"])
app.include_router(inventory.router, prefix=f"{api_prefix}/inventory", tags=["Inventory"])
app.include_router(promotions.router, prefix=f"{api_prefix}/promotions", tags=["Promotions"])
app.include_router(reviews.router, prefix=f"{api_prefix}/reviews", tags=["Reviews"])
app.include_router(admin.router, prefix=f"{api_prefix}/admin", tags=["Admin"])
