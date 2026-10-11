/**
 * Tests for categories API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { categoriesApi } from '../../src/api/categories';
import { apiClient } from '../../src/api/client';
import type { Category } from '../../src/types/category';
import type { PaginatedResponse } from '../../src/types/common';
import type { Product } from '../../src/types/product';

vi.mock('../../src/api/client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('categoriesApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getCategories', () => {
    it('should call GET /categories', async () => {
      const mockCategories: Category[] = [
        {
          id: 1,
          name: 'Electronics',
          description: 'Electronic devices',
          is_active: true,
          subcategories: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockCategories);

      const result = await categoriesApi.getCategories();

      expect(apiClient.get).toHaveBeenCalledWith('/categories');
      expect(result).toEqual(mockCategories);
    });

    it('should return empty array when no categories exist', async () => {
      (apiClient.get as any).mockResolvedValue([]);

      const result = await categoriesApi.getCategories();

      expect(result).toEqual([]);
    });

    it('should return hierarchical category structure', async () => {
      const mockCategories: Category[] = [
        {
          id: 1,
          name: 'Electronics',
          description: 'Electronic devices',
          is_active: true,
          subcategories: [
            {
              id: 2,
              name: 'Mobile Phones',
              description: 'Smartphones',
              parent_id: 1,
              is_active: true,
              subcategories: [],
              created_at: '2024-01-01T00:00:00Z',
              updated_at: '2024-01-01T00:00:00Z',
            },
          ],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockCategories);

      const result = await categoriesApi.getCategories();

      expect(result[0].subcategories).toHaveLength(1);
      expect(result[0].subcategories![0].name).toBe('Mobile Phones');
      expect(result[0].subcategories![0].parent_id).toBe(1);
    });
  });

  describe('getCategory', () => {
    it('should call GET /categories/:id', async () => {
      const mockCategory: Category = {
        id: 1,
        name: 'Electronics',
        description: 'Electronic devices',
        is_active: true,
        subcategories: [],
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.get as any).mockResolvedValue(mockCategory);

      const result = await categoriesApi.getCategory(1);

      expect(apiClient.get).toHaveBeenCalledWith('/categories/1');
      expect(result).toEqual(mockCategory);
    });

    it('should fetch category with parent_id', async () => {
      const mockCategory: Category = {
        id: 2,
        name: 'Mobile Phones',
        description: 'Smartphones',
        parent_id: 1,
        is_active: true,
        subcategories: [],
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.get as any).mockResolvedValue(mockCategory);

      const result = await categoriesApi.getCategory(2);

      expect(result.parent_id).toBe(1);
    });

    it('should handle non-existent category', async () => {
      const mockError = new Error('Category not found');
      (apiClient.get as any).mockRejectedValue(mockError);

      await expect(categoriesApi.getCategory(999)).rejects.toThrow('Category not found');
    });
  });

  describe('getCategoryProducts', () => {
    it('should call GET /categories/:id/products with no params', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [
          {
            id: 1,
            name: 'iPhone 15',
            description: 'Latest iPhone',
            brand: 'Apple',
            sku: 'APL-001',
            price: '999.99',
            category_id: 1,
            is_active: 'active',
            stock_status: 'in_stock',
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z',
          },
        ],
        total: 1,
        page: 1,
        per_page: 20,
        pages: 1,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await categoriesApi.getCategoryProducts(1);

      expect(apiClient.get).toHaveBeenCalledWith('/categories/1/products');
      expect(result).toEqual(mockResponse);
    });

    it('should call GET /categories/:id/products with pagination params', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [],
        total: 50,
        page: 2,
        per_page: 10,
        pages: 5,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await categoriesApi.getCategoryProducts(1, { page: 2, per_page: 10 });

      expect(apiClient.get).toHaveBeenCalledWith('/categories/1/products?page=2&per_page=10');
    });

    it('should handle empty category products', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [],
        total: 0,
        page: 1,
        per_page: 20,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await categoriesApi.getCategoryProducts(1);

      expect(result.items).toHaveLength(0);
      expect(result.total).toBe(0);
    });

    it('should handle non-existent category', async () => {
      const mockError = new Error('Category not found');
      (apiClient.get as any).mockRejectedValue(mockError);

      await expect(
        categoriesApi.getCategoryProducts(999)
      ).rejects.toThrow('Category not found');
    });

    it('should return products with stock status', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [
          {
            id: 1,
            name: 'Product 1',
            description: 'Test',
            brand: 'Brand',
            sku: 'SKU-001',
            price: '99.99',
            category_id: 1,
            is_active: 'active',
            stock_status: 'in_stock',
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z',
          },
          {
            id: 2,
            name: 'Product 2',
            description: 'Test',
            brand: 'Brand',
            sku: 'SKU-002',
            price: '49.99',
            category_id: 1,
            is_active: 'active',
            stock_status: 'low_stock',
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z',
          },
        ],
        total: 2,
        page: 1,
        per_page: 20,
        pages: 1,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await categoriesApi.getCategoryProducts(1);

      expect(result.items[0].stock_status).toBe('in_stock');
      expect(result.items[1].stock_status).toBe('low_stock');
    });

    it('should handle page param only', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [],
        total: 0,
        page: 3,
        per_page: 20,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await categoriesApi.getCategoryProducts(1, { page: 3 });

      expect(apiClient.get).toHaveBeenCalledWith('/categories/1/products?page=3');
    });

    it('should handle per_page param only', async () => {
      const mockResponse: PaginatedResponse<Product> = {
        items: [],
        total: 0,
        page: 1,
        per_page: 50,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await categoriesApi.getCategoryProducts(1, { per_page: 50 });

      expect(apiClient.get).toHaveBeenCalledWith('/categories/1/products?per_page=50');
    });
  });
});
