/**
 * Order API endpoints
 */

import { apiClient } from './client';
import type { OrderResponse, OrderStatusUpdate, OrderNoteCreate } from '../types/order';
import type { PaginatedResponse } from '../types/common';

export const ordersApi = {
  /**
   * Get current user's order history
   */
  getOrders: (params?: {
    page?: number;
    per_page?: number;
    customer_id?: number;
  }): Promise<PaginatedResponse<OrderResponse>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    if (params?.customer_id) searchParams.set('customer_id', params.customer_id.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<OrderResponse>>(`/orders${query ? `?${query}` : ''}`);
  },

  /**
   * Get order by ID
   */
  getOrder: (id: number): Promise<OrderResponse> =>
    apiClient.get<OrderResponse>(`/orders/${id}`),

  /**
   * Update order status (admin only)
   */
  updateOrderStatus: (id: number, data: OrderStatusUpdate): Promise<OrderResponse> =>
    apiClient.patch<OrderResponse>(`/orders/${id}/status`, data),

  /**
   * Add support note to order (customer support only)
   */
  addOrderNote: (id: number, data: OrderNoteCreate): Promise<void> =>
    apiClient.post<void>(`/orders/${id}/notes`, data),
};
