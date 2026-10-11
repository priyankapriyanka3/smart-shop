/**
 * Tests for products API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { productsApi } from '../../src/api/products';
import { apiClient } from '../../src/api/client';

vi.mock('../../src/api/client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('productsApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getProducts', () => {
    it('should call GET /products with default params', async () => {
      const mockResponse = {
        items: [{ id: 1, name: 'Product 1' }],
        total: 1,
        page: 1,
        per_page: 20,
        pages: 1,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await productsApi.getProducts();

      expect(apiClient.get).toHaveBeenCalledWith('/products');
      expect(result).toEqual(mockResponse);
    });

    it('should call GET /products with pagination params', async () => {
      const mockResponse = {
        items: [],
        total: 0,
        page: 2,
        per_page: 10,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await productsApi.getProducts({ page: 2, per_page: 10 });

      expect(apiClient.get).toHaveBeenCalledWith('/products?page=2&per_page=10');
    });

    it('should call GET /products with category filter', async () => {
      const mockResponse = {
        items: [],
        total: 0,
        page: 1,
        per_page: 20,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await productsApi.getProducts({ category_id: 5 });

      expect(apiClient.get).toHaveBeenCalledWith('/products?category_id=5');
    });
  });

  describe('getProduct', () => {
    it('should call GET /products/:id', async () => {
      const mockProduct = { id: 1, name: 'Product 1', price: '29.99' };
      (apiClient.get as any).mockResolvedValue(mockProduct);

      const result = await productsApi.getProduct(1);

      expect(apiClient.get).toHaveBeenCalledWith('/products/1');
      expect(result).toEqual(mockProduct);
    });
  });

  describe('createProduct', () => {
    it('should call POST /products', async () => {
      const newProduct = {
        name: 'New Product',
        description: 'Test description',
        brand: 'TestBrand',
        sku: 'TEST-001',
        price: '49.99',
        category_id: 1,
      };
      
      const mockResponse = { id: 1, ...newProduct };
      (apiClient.post as any).mockResolvedValue(mockResponse);

      const result = await productsApi.createProduct(newProduct);

      expect(apiClient.post).toHaveBeenCalledWith('/products', newProduct);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateProduct', () => {
    it('should call PUT /products/:id', async () => {
      const updates = { name: 'Updated Name', price: '59.99' };
      const mockResponse = { id: 1, ...updates };
      (apiClient.put as any).mockResolvedValue(mockResponse);

      const result = await productsApi.updateProduct(1, updates);

      expect(apiClient.put).toHaveBeenCalledWith('/products/1', updates);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('activateProduct', () => {
    it('should call PATCH /products/:id/activate', async () => {
      const mockResponse = { id: 1, is_active: 'true' };
      (apiClient.patch as any).mockResolvedValue(mockResponse);

      const result = await productsApi.activateProduct(1);

      expect(apiClient.patch).toHaveBeenCalledWith('/products/1/activate');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deactivateProduct', () => {
    it('should call PATCH /products/:id/deactivate', async () => {
      const mockResponse = { id: 1, is_active: 'false' };
      (apiClient.patch as any).mockResolvedValue(mockResponse);

      const result = await productsApi.deactivateProduct(1);

      expect(apiClient.patch).toHaveBeenCalledWith('/products/1/deactivate');
      expect(result).toEqual(mockResponse);
    });
  });
});
