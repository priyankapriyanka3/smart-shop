import { apiClient } from '../lib/api-client';
import type { Cart, CartItem } from '../types/cart';

export const cartService = {
  async getCart(): Promise<Cart> {
    return apiClient.get<Cart>('/cart');
  },

  async addItem(product_id: number, quantity: number = 1): Promise<Cart> {
    return apiClient.post<Cart>('/cart/items', { product_id, quantity });
  },

  async updateItem(item_id: number, quantity: number): Promise<Cart> {
    return apiClient.patch<Cart>(`/cart/items/${item_id}`, { quantity });
  },

  async removeItem(item_id: number): Promise<Cart> {
    return apiClient.delete<Cart>(`/cart/items/${item_id}`);
  },

  async applyPromoCode(promo_code: string): Promise<Cart> {
    return apiClient.post<Cart>('/cart/promo', { promo_code });
  },

  async clearCart(): Promise<void> {
    await apiClient.delete<void>('/cart');
  },
};
