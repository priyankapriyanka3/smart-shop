"""Pydantic schemas for request/response models."""

from app.schemas.category import CategoryList, CategoryResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate, CartResponse
from app.schemas.order import OrderResponse, OrderItemResponse, OrderStatusUpdate, OrderNoteCreate
from app.schemas.inventory import InventoryResponse, InventoryUpdate, LowStockItem
from app.schemas.discount import (
    DiscountCreate,
    DiscountUpdate,
    DiscountResponse,
    DiscountValidationRequest,
    DiscountValidationResponse,
)
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewHideRequest
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.schemas.common import PaginatedResponse

__all__ = [
    "CategoryList",
    "CategoryResponse",
    "ProductCreate",
    "ProductResponse",
    "ProductUpdate",
    "CartItemCreate",
    "CartItemResponse",
    "CartItemUpdate",
    "CartResponse",
    "OrderResponse",
    "OrderItemResponse",
    "OrderStatusUpdate",
    "OrderNoteCreate",
    "InventoryResponse",
    "InventoryUpdate",
    "LowStockItem",
    "DiscountCreate",
    "DiscountUpdate",
    "DiscountResponse",
    "DiscountValidationRequest",
    "DiscountValidationResponse",
    "ReviewCreate",
    "ReviewResponse",
    "ReviewHideRequest",
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierResponse",
    "PaginatedResponse",
]
