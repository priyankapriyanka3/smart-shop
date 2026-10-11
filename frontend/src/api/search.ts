/**
 * Search and discovery API endpoints
 */

import { apiClient } from './client';
import type { Product } from '../types/product';
import type { PaginatedResponse } from '../types/common';

export interface SearchParams {
  q?: string; // Search query
  page?: number;
  per_page?: number;
  category?: number;
  min_price?: number;
  max_price?: number;
  brand?: string;
  min_rating?: number;
  in_stock?: boolean;
  sort?: 'relevance' | 'price_asc' | 'price_desc' | 'rating' | 'newest';
}

export const searchApi = {
  /**
   * Search products with filters and sorting
   */
  searchProducts: (params: SearchParams): Promise<PaginatedResponse<Product>> => {
    const searchParams = new URLSearchParams();
    
    if (params.q) searchParams.set('q', params.q);
    if (params.page) searchParams.set('page', params.page.toString());
    if (params.per_page) searchParams.set('per_page', params.per_page.toString());
    if (params.category) searchParams.set('category', params.category.toString());
    if (params.min_price !== undefined) searchParams.set('min_price', params.min_price.toString());
    if (params.max_price !== undefined) searchParams.set('max_price', params.max_price.toString());
    if (params.brand) searchParams.set('brand', params.brand);
    if (params.min_rating !== undefined) searchParams.set('min_rating', params.min_rating.toString());
    if (params.in_stock !== undefined) searchParams.set('in_stock', params.in_stock.toString());
    if (params.sort) searchParams.set('sort', params.sort);
    
    return apiClient.get<PaginatedResponse<Product>>(`/search?${searchParams.toString()}`);
  },
};
