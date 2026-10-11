"""Pydantic schemas for request/response models."""

from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate, CartResponse
from app.schemas.category import CategoryList, CategoryResponse
from app.schemas.common import PaginatedResponse
from app.schemas.discount import (
    DiscountCreate,
    DiscountResponse,
    DiscountUpdate,
    DiscountValidationRequest,
    DiscountValidationResponse,
)
from app.schemas.inventory import InventoryResponse, InventoryUpdate, LowStockItem
from app.schemas.order import OrderItemResponse, OrderNoteCreate, OrderResponse, OrderStatusUpdate
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.review import ReviewCreate, ReviewHideRequest, ReviewResponse
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate

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
