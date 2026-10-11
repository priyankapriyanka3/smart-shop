"""Pydantic schemas for request/response validation."""
from app.schemas.catalog import (
    CategoryBase,
    CategoryCreate,
    CategoryResponse,
    ProductBase,
    ProductCreate,
    ProductResponse,
    ProductListResponse,
    CategoryListResponse,
)
from app.schemas.customers import (
    UserBase,
    UserCreate,
    UserResponse,
    UserListResponse,
    AddressBase,
    AddressCreate,
    AddressResponse,
    AddressListResponse,
)
from app.schemas.cart import (
    CartBase,
    CartResponse,
    CartItemBase,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
)
from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutValidationResponse,
)
from app.schemas.orders import (
    OrderBase,
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderItemBase,
    OrderItemResponse,
)
from app.schemas.payments import (
    PaymentBase,
    PaymentCreate,
    PaymentResponse,
)
from app.schemas.inventory import (
    WarehouseBase,
    WarehouseCreate,
    WarehouseResponse,
    SupplierBase,
    SupplierCreate,
    SupplierResponse,
    InventoryBase,
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryListResponse,
)
from app.schemas.promotions import (
    PromotionBase,
    PromotionCreate,
    PromotionUpdate,
    PromotionResponse,
    PromotionListResponse,
    PromotionEligibilityResponse,
)
from app.schemas.reviews import (
    ReviewBase,
    ReviewCreate,
    ReviewResponse,
    ReviewListResponse,
    ReviewModerationRequest,
)
from app.schemas.admin import (
    StatsResponse,
    DashboardResponse,
)

__all__ = [
    # Catalog
    "CategoryBase",
    "CategoryCreate",
    "CategoryResponse",
    "ProductBase",
    "ProductCreate",
    "ProductResponse",
    "ProductListResponse",
    "CategoryListResponse",
    # Customers
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserListResponse",
    "AddressBase",
    "AddressCreate",
    "AddressResponse",
    "AddressListResponse",
    # Cart
    "CartBase",
    "CartResponse",
    "CartItemBase",
    "CartItemCreate",
    "CartItemUpdate",
    "CartItemResponse",
    # Checkout
    "CheckoutRequest",
    "CheckoutValidationResponse",
    # Orders
    "OrderBase",
    "OrderCreate",
    "OrderResponse",
    "OrderListResponse",
    "OrderItemBase",
    "OrderItemResponse",
    # Payments
    "PaymentBase",
    "PaymentCreate",
    "PaymentResponse",
    # Inventory
    "WarehouseBase",
    "WarehouseCreate",
    "WarehouseResponse",
    "SupplierBase",
    "SupplierCreate",
    "SupplierResponse",
    "InventoryBase",
    "InventoryCreate",
    "InventoryUpdate",
    "InventoryResponse",
    "InventoryListResponse",
    # Promotions
    "PromotionBase",
    "PromotionCreate",
    "PromotionUpdate",
    "PromotionResponse",
    "PromotionListResponse",
    "PromotionEligibilityResponse",
    # Reviews
    "ReviewBase",
    "ReviewCreate",
    "ReviewResponse",
    "ReviewListResponse",
    "ReviewModerationRequest",
    # Admin
    "StatsResponse",
    "DashboardResponse",
]
