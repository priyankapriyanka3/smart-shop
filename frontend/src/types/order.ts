/**
 * Order types matching backend Pydantic models
 */

export interface OrderItemResponse {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string;
  product_brand: string;
  quantity: number;
  unit_price: string; // Decimal from backend serialized as string
  subtotal: string; // Decimal from backend serialized as string
  created_at: string;
}

export interface OrderResponse {
  id: number;
  customer_id: number;
  order_date: string;
  total_amount: string; // Decimal from backend serialized as string
  status: string; // "pending", "confirmed", "shipped", "delivered"
  delivery_address: string;
  discount_code?: string | null;
  items: OrderItemResponse[];
  created_at: string;
  updated_at: string;
}

export interface OrderStatusUpdate {
  status: string; // "pending", "confirmed", "shipped", "delivered"
}

export interface OrderNoteCreate {
  note: string;
}
