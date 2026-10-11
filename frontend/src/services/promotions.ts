/**
 * Promotions service for discount campaign management
 */

import { apiClient } from '../lib/api-client';
import { Promotion, PromotionCreateRequest } from '../types/admin';
import { PaginatedResponse } from '../types/catalog';

/**
 * Get promotions with pagination
 */
export async function getPromotions(params?: {
  page?: number;
  page_size?: number;
  is_active?: boolean;
}): Promise<PaginatedResponse<Promotion>> {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set('page', params.page.toString());
  if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
  if (params?.is_active !== undefined) searchParams.set('is_active', params.is_active.toString());
  
  const queryString = searchParams.toString();
  const url = `/promotions${queryString ? `?${queryString}` : ''}`;
  
  return apiClient.get<PaginatedResponse<Promotion>>(url);
}

/**
 * Create new promotion
 */
export async function createPromotion(data: PromotionCreateRequest): Promise<Promotion> {
  return apiClient.post<Promotion>('/promotions', data);
}

/**
 * Update promotion
 */
export async function updatePromotion(
  promotionId: number,
  data: Partial<PromotionCreateRequest>
): Promise<Promotion> {
  return apiClient.patch<Promotion>(`/promotions/${promotionId}`, data);
}

/**
 * Activate/deactivate promotion
 */
export async function togglePromotionStatus(
  promotionId: number,
  isActive: boolean
): Promise<Promotion> {
  return apiClient.patch<Promotion>(`/promotions/${promotionId}/status`, { is_active: isActive });
}

/**
 * Validate promotion code
 */
export async function validatePromotion(code: string): Promise<{
  valid: boolean;
  promotion?: Promotion;
  message?: string;
}> {
  return apiClient.post<{ valid: boolean; promotion?: Promotion; message?: string }>(
    '/promotions/validate',
    { code }
  );
}
