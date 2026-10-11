/**
 * Catalog domain types matching backend schemas
 */

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Category matching backend CategoryResponse schema
 */
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  parent_id: number | null;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * Product matching backend ProductResponse schema
 */
export interface Product {
  id: number;
  category_id: number;
  sku: string;
  name: string;
  slug: string;
  brand: string | null;
  description: string | null;
  price: number;
  image_url: string | null;
  status: string;
  available_quantity: number | null;
  created_at: string;
  updated_at: string;
}

/**
 * Product search/filter request
 */
export interface ProductSearchRequest {
  query?: string;
  category_id?: number;
  min_price?: number;
  max_price?: number;
  brand?: string;
  min_rating?: number;
  in_stock?: boolean;
  sort_by?: 'relevance' | 'price_asc' | 'price_desc' | 'newest' | 'rating';
  page?: number;
  page_size?: number;
}

/**
 * Cart item matching backend CartItemResponse schema
 */
export interface CartItem {
  id: number;
  cart_id: number;
  product_id: number;
  quantity: number;
  product_name: string;
  product_price: number;
  product_image_url: string | null;
  subtotal: number;
  created_at: string;
  updated_at: string;
}

/**
 * Cart matching backend CartResponse schema
 */
export interface Cart {
  id: number;
  customer_id: number;
  status: string;
  items: CartItem[];
  subtotal: number;
  total_items: number;
  created_at: string;
  updated_at: string;
}

/**
 * Add to cart request
 */
export interface AddToCartRequest {
  product_id: number;
  quantity: number;
}

/**
 * Update cart item request
 */
export interface UpdateCartItemRequest {
  quantity: number;
}
