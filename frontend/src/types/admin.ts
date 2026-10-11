/**
 * Admin domain types matching backend schemas
 */

/**
 * Inventory record matching backend InventoryResponse schema
 */
export interface Inventory {
  id: number;
  product_id: number;
  warehouse_id: number;
  quantity: number;
  reorder_level: number;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * Warehouse matching backend WarehouseResponse schema
 */
export interface Warehouse {
  id: number;
  name: string;
  location: string;
  created_at: string;
  updated_at: string;
}

/**
 * Supplier matching backend SupplierResponse schema
 */
export interface Supplier {
  id: number;
  name: string;
  contact_email: string;
  lead_time_days: number;
  created_at: string;
  updated_at: string;
}

/**
 * Promotion matching backend PromotionResponse schema
 */
export interface Promotion {
  id: number;
  code: string;
  discount_type: string;
  discount_value: number;
  min_order_amount: number;
  max_uses: number | null;
  usage_count: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Promotion creation request
 */
export interface PromotionCreateRequest {
  code: string;
  discount_type: 'percentage' | 'fixed' | 'free_shipping';
  discount_value: number;
  min_order_amount: number;
  max_uses?: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
}

/**
 * Dashboard stats
 */
export interface DashboardStats {
  total_orders: number;
  total_revenue: number;
  low_stock_items: number;
  pending_reviews: number;
  orders_trend: number;
  revenue_trend: number;
}
