"""Inventory domain schemas: Warehouses, Suppliers, and Inventory records."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class WarehouseBase(BaseModel):
    """Base warehouse schema."""
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=500)
    status: str = Field(default="active", pattern="^(active|inactive)$")


class WarehouseCreate(WarehouseBase):
    """Warehouse creation request."""
    pass


class WarehouseResponse(WarehouseBase):
    """Warehouse response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SupplierBase(BaseModel):
    """Base supplier schema."""
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=100)
    contact_email: Optional[EmailStr] = None
    lead_time_days: int = Field(default=7, ge=0)
    status: str = Field(default="active", pattern="^(active|inactive)$")


class SupplierCreate(SupplierBase):
    """Supplier creation request."""
    pass


class SupplierResponse(SupplierBase):
    """Supplier response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class InventoryBase(BaseModel):
    """Base inventory schema."""
    product_id: int = Field(..., gt=0)
    warehouse_id: int = Field(..., gt=0)
    supplier_id: Optional[int] = Field(None, gt=0)
    quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=10, ge=0)
    status: str = Field(
        default="in_stock",
        pattern="^(in_stock|low_stock|out_of_stock)$"
    )


class InventoryCreate(InventoryBase):
    """Inventory creation request."""
    pass


class InventoryUpdate(BaseModel):
    """Inventory update request."""
    quantity: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(
        None,
        pattern="^(in_stock|low_stock|out_of_stock)$"
    )


class InventoryResponse(InventoryBase):
    """Inventory response with product and warehouse details."""
    id: int
    product_name: str
    product_sku: str
    warehouse_name: str
    warehouse_code: str
    supplier_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class InventoryListResponse(BaseModel):
    """Paginated inventory list response."""
    items: List[InventoryResponse]
    total: int
    page: int
    page_size: int


class StockUpdateRequest(BaseModel):
    """Stock quantity update request (set to specific value)."""
    quantity: int = Field(..., ge=0)
    reason: str = Field(..., min_length=1, max_length=500)


class StockAdjustmentRequest(BaseModel):
    """Stock adjustment request (relative change)."""
    adjustment: int
    reason: str = Field(..., min_length=1, max_length=500)


class StockAdjustmentRequestFull(BaseModel):
    """Stock adjustment request with inventory_id (legacy format)."""
    inventory_id: int = Field(..., gt=0)
    quantity_change: int
    reason: str = Field(..., min_length=1, max_length=500)


class LowStockResponse(BaseModel):
    """Low stock alert response."""
    items: List[InventoryResponse]
    total: int
    page: int
    page_size: int


class ReplenishmentPriorityResponse(BaseModel):
    """Replenishment priority item."""
    inventory_id: int
    product_id: int
    product_name: str
    product_sku: str
    warehouse_name: str
    current_quantity: int
    reorder_level: int
    shortage: int
    supplier_lead_time_days: int
    priority_score: float
