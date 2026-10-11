/**
 * Discount/Promotion API endpoints
 */

import { apiClient } from './client';
import type {
  Discount,
  DiscountCreate,
  DiscountUpdate,
  DiscountValidateRequest,
  DiscountValidateResponse,
} from '../types/discount';
import type { PaginatedResponse } from '../types/common';

export const discountsApi = {
  /**
   * Get paginated discounts (admin only)
   */
  getDiscounts: (params?: {
    page?: number;
    per_page?: number;
  }): Promise<PaginatedResponse<Discount>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Discount>>(`/discounts${query ? `?${query}` : ''}`);
  },

  /**
   * Create discount (admin only)
   */
  createDiscount: (data: DiscountCreate): Promise<Discount> =>
    apiClient.post<Discount>('/discounts', data),

  /**
   * Update discount (admin only)
   */
  updateDiscount: (id: number, data: DiscountUpdate): Promise<Discount> =>
    apiClient.put<Discount>(`/discounts/${id}`, data),

  /**
   * Validate discount code for cart
   */
  validateDiscount: (data: DiscountValidateRequest): Promise<DiscountValidateResponse> =>
    apiClient.post<DiscountValidateResponse>('/discounts/validate', data),
};
