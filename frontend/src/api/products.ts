/**
 * Product API endpoints
 */

import { apiClient } from './client';
import type { Product, ProductCreate, ProductUpdate } from '../types/product';
import type { PaginatedResponse } from '../types/common';

// Named exports for convenience
export const getProducts = (params?: {
  page?: number;
  per_page?: number;
  category_id?: number;
}): Promise<PaginatedResponse<Product>> => productsApi.getProducts(params);

export const getProduct = (id: number): Promise<Product> => productsApi.getProduct(id);

export const productsApi = {
  /**
   * Get paginated list of active products
   */
  getProducts: (params?: {
    page?: number;
    per_page?: number;
    category_id?: number;
  }): Promise<PaginatedResponse<Product>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    if (params?.category_id) searchParams.set('category_id', params.category_id.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Product>>(`/products${query ? `?${query}` : ''}`);
  },

  /**
   * Get product by ID
   */
  getProduct: (id: number): Promise<Product> =>
    apiClient.get<Product>(`/products/${id}`),

  /**
   * Create new product (admin only)
   */
  createProduct: (data: ProductCreate): Promise<Product> =>
    apiClient.post<Product>('/products', data),

  /**
   * Update product (admin only)
   */
  updateProduct: (id: number, data: ProductUpdate): Promise<Product> =>
    apiClient.put<Product>(`/products/${id}`, data),

  /**
   * Activate product (admin only)
   */
  activateProduct: (id: number): Promise<Product> =>
    apiClient.patch<Product>(`/products/${id}/activate`),

  /**
   * Deactivate product (admin only)
   */
  deactivateProduct: (id: number): Promise<Product> =>
    apiClient.patch<Product>(`/products/${id}/deactivate`),
};
