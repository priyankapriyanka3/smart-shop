/**
 * Review types matching backend Pydantic models
 */

export interface ReviewBase {
  product_id: number;
  rating: number; // 1-5
  review_text: string;
}

export interface Review extends ReviewBase {
  id: number;
  customer_id: number;
  helpful_count: number;
  is_hidden: string;
  created_at: string;
  updated_at: string;
  customer?: {
    id: number;
    full_name: string;
    email: string;
  };
}

export interface ReviewCreate extends ReviewBase {}

export interface ReviewModerate {
  is_hidden: string; // "true" or "false"
}
