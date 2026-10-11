"""Inventory domain service: Stock management and replenishment priority."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.inventory import Inventory, Warehouse, Supplier
from app.models.catalog import Product
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryListResponse,
    ReplenishmentPriorityResponse,
)


class InventoryService:
    """Service for inventory operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_inventory_response(self, inventory: Inventory) -> InventoryResponse:
        """Build inventory response with enriched data."""
        return InventoryResponse(
            id=inventory.id,
            product_id=inventory.product_id,
            warehouse_id=inventory.warehouse_id,
            supplier_id=inventory.supplier_id,
            quantity=inventory.quantity,
            reorder_level=inventory.reorder_level,
            status=inventory.status,
            product_name=inventory.product.name,
            product_sku=inventory.product.sku,
            warehouse_name=inventory.warehouse.name,
            warehouse_code=inventory.warehouse.code,
            supplier_name=inventory.supplier.name if inventory.supplier else None,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )

    def get_inventory(
        self,
        page: int = 1,
        page_size: int = 20,
        product_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> InventoryListResponse:
        """Get paginated list of inventory records."""
        query = self.db.query(Inventory)

        if product_id:
            query = query.filter(Inventory.product_id == product_id)

        if warehouse_id:
            query = query.filter(Inventory.warehouse_id == warehouse_id)

        if status:
            query = query.filter(Inventory.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        inventory_records = query.offset(offset).limit(page_size).all()

        return InventoryListResponse(
            items=[self.get_inventory_response(inv) for inv in inventory_records],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_inventory_list(
        self,
        page: int = 1,
        page_size: int = 20,
        warehouse_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> InventoryListResponse:
        """Get paginated list of inventory records (alias for backwards compatibility)."""
        return self.get_inventory(
            page=page,
            page_size=page_size,
            warehouse_id=warehouse_id,
            status=status,
        )

    def get_inventory_by_id(self, inventory_id: int) -> Optional[InventoryResponse]:
        """Get inventory record by ID."""
        inventory = self.db.query(Inventory).filter(Inventory.id == inventory_id).first()
        return self.get_inventory_response(inventory) if inventory else None

    def get_inventory_by_product_warehouse(
        self,
        product_id: int,
        warehouse_id: int,
    ) -> Optional[InventoryResponse]:
        """Get inventory record for specific product and warehouse."""
        inventory = (
            self.db.query(Inventory)
            .filter(
                and_(
                    Inventory.product_id == product_id,
                    Inventory.warehouse_id == warehouse_id,
                )
            )
            .first()
        )
        return self.get_inventory_response(inventory) if inventory else None

    def create_inventory(self, data: InventoryCreate) -> InventoryResponse:
        """Create inventory record."""
        # Determine status based on quantity
        if data.quantity == 0:
            status = "out_of_stock"
        elif data.quantity <= data.reorder_level:
            status = "low_stock"
        else:
            status = "in_stock"

        inventory = Inventory(
            **data.model_dump(),
            status=status,
        )
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return self.get_inventory_response(inventory)

    def update_inventory(
        self,
        inventory_id: int,
        data: InventoryUpdate,
    ) -> Optional[InventoryResponse]:
        """Update inventory record."""
        inventory = self.db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inventory:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(inventory, key, value)

        # Auto-update status based on quantity if not explicitly set
        if data.quantity is not None and data.status is None:
            if inventory.quantity == 0:
                inventory.status = "out_of_stock"
            elif inventory.quantity <= inventory.reorder_level:
                inventory.status = "low_stock"
            else:
                inventory.status = "in_stock"

        self.db.commit()
        self.db.refresh(inventory)
        return self.get_inventory_response(inventory)

    def adjust_stock(
        self,
        inventory_id: int,
        quantity_change: int,
        reason: str,
        user_id: Optional[int] = None,
    ) -> Optional[InventoryResponse]:
        """Adjust inventory stock level with audit logging."""
        from app.audit.logger import log_audit
        
        inventory = self.db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inventory:
            return None

        old_quantity = inventory.quantity
        new_quantity = inventory.quantity + quantity_change
        
        # Prevent negative stock
        if new_quantity < 0:
            raise ValueError("Insufficient stock for adjustment")
        
        inventory.quantity = new_quantity

        # Update status
        if new_quantity == 0:
            inventory.status = "out_of_stock"
        elif new_quantity <= inventory.reorder_level:
            inventory.status = "low_stock"
        else:
            inventory.status = "in_stock"

        self.db.commit()
        self.db.refresh(inventory)
        
        # Log audit entry for stock adjustment
        if user_id:
            log_audit(
                db=self.db,
                user_id=user_id,
                object_type="inventory",
                object_id=inventory_id,
                action="adjust",
                summary=f"Stock adjusted for {inventory.product.sku} from {old_quantity} to {new_quantity}. Reason: {reason}",
            )
        
        return self.get_inventory_response(inventory)

    def get_product_total_stock(self, product_id: int) -> Optional[InventoryResponse]:
        """Get total available stock for a product across all warehouses."""
        # Get first inventory record for the product
        inventory = (
            self.db.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .first()
        )
        if not inventory:
            return None
        
        # Calculate total quantity across all warehouses
        total_quantity = (
            self.db.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .with_entities(Inventory.quantity)
            .all()
        )
        total = sum(q[0] for q in total_quantity)
        
        # Return the first inventory record but with total quantity
        response = self.get_inventory_response(inventory)
        response.quantity = total
        return response

    def get_low_stock_items(
        self,
        page: int = 1,
        page_size: int = 20,
    ):
        """Get list of products with stock below reorder level."""
        from app.schemas.inventory import LowStockResponse
        
        query = self.db.query(Inventory).filter(
            Inventory.status.in_(["low_stock", "out_of_stock"])
        )
        
        total = query.count()
        offset = (page - 1) * page_size
        inventory_records = query.offset(offset).limit(page_size).all()
        
        return LowStockResponse(
            items=[self.get_inventory_response(inv) for inv in inventory_records],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_replenishment_priorities(
        self,
        limit: int = 50,
    ) -> list[ReplenishmentPriorityResponse]:
        """Get inventory items needing replenishment, prioritized."""
        # Get low stock and out of stock items
        inventory_records = (
            self.db.query(Inventory)
            .filter(Inventory.status.in_(["low_stock", "out_of_stock"]))
            .all()
        )

        priorities = []
        for inv in inventory_records:
            shortage = max(0, inv.reorder_level - inv.quantity)
            lead_time = inv.supplier.lead_time_days if inv.supplier else 14

            # Priority score: higher shortage and shorter lead time = higher priority
            priority_score = (shortage * 10.0) / max(lead_time, 1)

            priorities.append(
                ReplenishmentPriorityResponse(
                    inventory_id=inv.id,
                    product_id=inv.product_id,
                    product_name=inv.product.name,
                    product_sku=inv.product.sku,
                    warehouse_name=inv.warehouse.name,
                    current_quantity=inv.quantity,
                    reorder_level=inv.reorder_level,
                    shortage=shortage,
                    supplier_lead_time_days=lead_time,
                    priority_score=priority_score,
                )
            )

        # Sort by priority score descending
        priorities.sort(key=lambda x: x.priority_score, reverse=True)
        return priorities[:limit]
