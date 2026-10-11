/**
 * Orders domain types matching backend schemas
 */

import { Product } from './catalog';

/**
 * Order item matching backend OrderItemResponse schema
 */
export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string;
  product_sku: string;
  product?: Product;
  quantity: number;
  unit_price: number;
  total_price: number;
  created_at: string;
  updated_at: string;
}

/**
 * Order matching backend OrderResponse schema
 */
export interface Order {
  id: number;
  order_number: string;
  customer_id: number;
  status: string;
  subtotal: number;
  discount_amount: number;
  shipping_cost: number;
  total: number;
  shipping_street: string;
  shipping_city: string;
  shipping_state_province: string;
  shipping_postal_code: string;
  shipping_country: string;
  billing_street: string;
  billing_city: string;
  billing_state_province: string;
  billing_postal_code: string;
  billing_country: string;
  promotion_code: string | null;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

/**
 * Order creation request
 */
export interface OrderCreateRequest {
  shipping_address_id: number;
  billing_address_id: number;
  promotion_code?: string;
  payment_method: string;
}

/**
 * Payment matching backend PaymentResponse schema
 */
export interface Payment {
  id: number;
  order_id: number;
  amount: number;
  currency: string;
  state: string;
  external_ref: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Review matching backend ReviewResponse schema
 */
export interface Review {
  id: number;
  product_id: number;
  customer_id: number;
  rating: number;
  review_text: string | null;
  status: string;
  helpful_count: number;
  created_at: string;
  updated_at: string;
}

/**
 * Review submission request
 */
export interface ReviewCreateRequest {
  product_id: number;
  rating: number;
  review_text?: string;
}
