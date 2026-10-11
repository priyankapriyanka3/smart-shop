export interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  product_brand?: string;
  product_image_url?: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  availability: string;
  created_at: string;
  updated_at: string;
}

export interface Cart {
  id: number;
  customer_id: number;
  items: CartItem[];
  subtotal: number;
  discount: number;
  shipping: number;
  tax: number;
  total: number;
  promo_code?: string;
  item_count: number;
  created_at: string;
  updated_at: string;
}
