/**
 * Category API endpoints
 */

import { apiClient } from './client';
import type { Category } from '../types/category';
import type { Product } from '../types/product';
import type { PaginatedResponse } from '../types/common';

// Named exports for convenience
export const getCategories = (): Promise<Category[]> => categoriesApi.getCategories();

export const categoriesApi = {
  /**
   * Get hierarchical list of categories
   */
  getCategories: (): Promise<Category[]> =>
    apiClient.get<Category[]>('/categories'),

  /**
   * Get category by ID
   */
  getCategory: (id: number): Promise<Category> =>
    apiClient.get<Category>(`/categories/${id}`),

  /**
   * Get paginated products in a category
   */
  getCategoryProducts: (
    id: number,
    params?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Product>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Product>>(
      `/categories/${id}/products${query ? `?${query}` : ''}`
    );
  },
};
