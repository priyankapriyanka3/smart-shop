/**
 * Discount types matching backend Pydantic models
 */

export interface DiscountBase {
  code: string;
  discount_type: string; // "percentage" or "fixed_amount"
  discount_value: string; // Decimal from backend serialized as string
  min_order_amount?: string | null; // Decimal from backend serialized as string
  valid_from: string;
  valid_to: string;
  max_uses?: number | null;
}

export interface Discount extends DiscountBase {
  id: number;
  times_used: number;
  is_active: string;
  created_at: string;
  updated_at: string;
}

export interface DiscountCreate extends DiscountBase {}

export interface DiscountUpdate {
  discount_type?: string;
  discount_value?: string;
  min_order_amount?: string | null;
  valid_from?: string;
  valid_to?: string;
  max_uses?: number | null;
  is_active?: string;
}

export interface DiscountValidateRequest {
  code: string;
  cart_total: string; // Decimal from backend serialized as string
}

export interface DiscountValidateResponse {
  valid: boolean;
  discount?: Discount;
  message?: string;
}
