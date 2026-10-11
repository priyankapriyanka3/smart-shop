/**
 * Inventory types matching backend Pydantic models
 */

export interface InventoryBase {
  product_id: number;
  warehouse_id: number;
  quantity: number;
  reorder_level: number;
}

export interface Inventory extends InventoryBase {
  id: number;
  last_updated: string;
  product_name?: string;
  warehouse_name?: string;
  created_at: string;
  updated_at: string;
}

export interface InventoryUpdate {
  quantity: number;
}

export interface LowStockItem {
  id: number;
  product_id: number;
  product_name: string;
  sku: string;
  warehouse_id: number;
  warehouse_name: string;
  quantity: number;
  reorder_level: number;
  supplier_id?: number | null;
  supplier_name?: string | null;
  lead_time_days?: number | null;
}
