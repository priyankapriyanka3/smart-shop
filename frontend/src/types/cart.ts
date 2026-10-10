/**
 * Cart types matching backend Pydantic models
 */

export interface ProductSummary {
  id: number;
  name: string;
  brand: string;
  price: string; // Decimal from backend serialized as string
  sku: string;
  stock_status?: string | null;
}

export interface CartItemBase {
  product_id: number;
  quantity: number;
}

export interface CartItem {
  id: number;
  cart_id: number;
  product_id: number;
  quantity: number;
  product: ProductSummary;
  created_at: string;
  updated_at: string;
}

export interface CartItemCreate extends CartItemBase {}

export interface CartItemUpdate {
  quantity: number;
}

export interface Cart {
  id: number;
  customer_id: number;
  items: CartItem[];
  total_items: number;
  subtotal: string; // Decimal from backend serialized as string
  created_at: string;
  updated_at: string;
}
