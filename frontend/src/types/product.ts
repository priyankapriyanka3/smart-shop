/**
 * Product types matching backend Pydantic models
 */

export interface ProductBase {
  name: string;
  description: string;
  brand: string;
  sku: string;
  price: string; // Decimal from backend serialized as string
  category_id: number;
}

export interface Product extends ProductBase {
  id: number;
  is_active: string; // Backend returns "1" or "0"
  stock_status?: string | null; // "in_stock", "low_stock", "out_of_stock"
  avg_rating?: number | null;
  review_count?: number | null;
  created_at: string;
  updated_at: string;
}

export interface ProductCreate extends ProductBase {}

export interface ProductUpdate {
  name?: string;
  description?: string;
  brand?: string;
  sku?: string;
  price?: string;
  category_id?: number;
}
