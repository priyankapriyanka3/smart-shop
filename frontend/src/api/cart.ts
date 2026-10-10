/**
 * Cart API endpoints
 */

import { apiClient } from './client';
import type { Cart, CartItemCreate, CartItemUpdate } from '../types/cart';

export const cartApi = {
  /**
   * Get current user's cart
   */
  getCart: (): Promise<Cart> =>
    apiClient.get<Cart>('/cart'),

  /**
   * Add item to cart
   */
  addItem: (data: CartItemCreate): Promise<Cart> =>
    apiClient.post<Cart>('/cart/items', data),

  /**
   * Update cart item quantity
   */
  updateItem: (itemId: number, data: CartItemUpdate): Promise<Cart> =>
    apiClient.put<Cart>(`/cart/items/${itemId}`, data),

  /**
   * Remove item from cart
   */
  removeItem: (itemId: number): Promise<Cart> =>
    apiClient.delete<Cart>(`/cart/items/${itemId}`),
};
