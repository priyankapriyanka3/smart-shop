import { apiClient } from '../lib/api-client';
import type { Product, Category, PaginatedResponse } from '../types/catalog';

export const catalogService = {
  async getCategories(): Promise<PaginatedResponse<Category>> {
    return apiClient.get<PaginatedResponse<Category>>('/catalog/categories');
  },

  async getCategoryBySlug(slug: string): Promise<Category> {
    return apiClient.get<Category>(`/catalog/categories/${slug}`);
  },

  async getProducts(params?: {
    category_id?: number;
    search?: string;
    min_price?: number;
    max_price?: number;
    brand?: string;
    rating?: number;
    in_stock?: boolean;
    sort_by?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Product>> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
    }
    const query = queryParams.toString();
    return apiClient.get<PaginatedResponse<Product>>(
      `/catalog/products${query ? `?${query}` : ''}`
    );
  },

  async getProductById(id: number): Promise<Product> {
    return apiClient.get<Product>(`/catalog/products/${id}`);
  },

  async searchProducts(query: string, params?: {
    min_price?: number;
    max_price?: number;
    brand?: string;
    rating?: number;
    in_stock?: boolean;
    sort_by?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Product>> {
    const queryParams = new URLSearchParams({ q: query });
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
    }
    return apiClient.get<PaginatedResponse<Product>>(
      `/catalog/search?${queryParams.toString()}`
    );
  },

  async getFeaturedProducts(limit: number = 8): Promise<Product[]> {
    const response = await apiClient.get<PaginatedResponse<Product>>(
      `/catalog/products?page_size=${limit}&featured=true`
    );
    return Array.isArray(response) ? response : response.items || [];
  },

  async getRelatedProducts(productId: number, limit: number = 4): Promise<Product[]> {
    const response = await apiClient.get<PaginatedResponse<Product>>(
      `/catalog/products/${productId}/related?page_size=${limit}`
    );
    return Array.isArray(response) ? response : response.items || [];
  },

  async getProductReviews(productId: number): Promise<any[]> {
    const response = await apiClient.get<any>(
      `/reviews/products/${productId}`
    );
    return Array.isArray(response) ? response : response.items || [];
  },
};
