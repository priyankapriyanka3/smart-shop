import { apiClient } from '../lib/api-client';
import type { Order } from '../types/orders';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export const ordersService = {
  async getOrders(params?: {
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Order>> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
    }
    const query = queryParams.toString();
    return apiClient.get<PaginatedResponse<Order>>(
      `/orders${query ? `?${query}` : ''}`
    );
  },

  async getOrderById(id: number): Promise<Order> {
    return apiClient.get<Order>(`/orders/${id}`);
  },

  async createOrder(data: {
    shipping_address_id: number;
    billing_address_id: number;
    payment_method: string;
    promo_code?: string;
  }): Promise<Order> {
    return apiClient.post<Order>('/checkout/submit', data);
  },

  async validateCheckout(data: {
    shipping_address_id: number;
    billing_address_id: number;
  }): Promise<{ valid: boolean; errors?: string[] }> {
    return apiClient.post<{ valid: boolean; errors?: string[] }>(
      '/checkout/validate',
      data
    );
  },
};
