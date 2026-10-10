/**
 * Tests for cart API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { cartApi } from '../../src/api/cart';
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

describe('cartApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getCart', () => {
    it('should call GET /cart', async () => {
      const mockCart = {
        id: 1,
        customer_id: 1,
        items: [],
        total_items: 0,
        subtotal: '0.00',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.get as any).mockResolvedValue(mockCart);

      const result = await cartApi.getCart();

      expect(apiClient.get).toHaveBeenCalledWith('/cart');
      expect(result).toEqual(mockCart);
    });
  });

  describe('addItem', () => {
    it('should call POST /cart/items', async () => {
      const itemData = { product_id: 1, quantity: 2 };
      const mockCart = {
        id: 1,
        customer_id: 1,
        items: [{ id: 1, ...itemData }],
        total_items: 2,
        subtotal: '59.98',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.post as any).mockResolvedValue(mockCart);

      const result = await cartApi.addItem(itemData);

      expect(apiClient.post).toHaveBeenCalledWith('/cart/items', itemData);
      expect(result).toEqual(mockCart);
    });
  });

  describe('updateItem', () => {
    it('should call PUT /cart/items/:id', async () => {
      const updateData = { quantity: 3 };
      const mockCart = {
        id: 1,
        customer_id: 1,
        items: [],
        total_items: 3,
        subtotal: '89.97',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.put as any).mockResolvedValue(mockCart);

      const result = await cartApi.updateItem(1, updateData);

      expect(apiClient.put).toHaveBeenCalledWith('/cart/items/1', updateData);
      expect(result).toEqual(mockCart);
    });
  });

  describe('removeItem', () => {
    it('should call DELETE /cart/items/:id', async () => {
      const mockCart = {
        id: 1,
        customer_id: 1,
        items: [],
        total_items: 0,
        subtotal: '0.00',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      };
      
      (apiClient.delete as any).mockResolvedValue(mockCart);

      const result = await cartApi.removeItem(1);

      expect(apiClient.delete).toHaveBeenCalledWith('/cart/items/1');
      expect(result).toEqual(mockCart);
    });
  });
});
