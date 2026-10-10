/**
 * Supplier API endpoints
 */

import { apiClient } from './client';
import type { Supplier, SupplierCreate, SupplierUpdate } from '../types/supplier';
import type { PaginatedResponse } from '../types/common';

export const suppliersApi = {
  /**
   * Get paginated suppliers (inventory_manager role)
   */
  getSuppliers: (params?: {
    page?: number;
    per_page?: number;
  }): Promise<PaginatedResponse<Supplier>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Supplier>>(`/suppliers${query ? `?${query}` : ''}`);
  },

  /**
   * Create supplier (inventory_manager role)
   */
  createSupplier: (data: SupplierCreate): Promise<Supplier> =>
    apiClient.post<Supplier>('/suppliers', data),

  /**
   * Update supplier (inventory_manager role)
   */
  updateSupplier: (id: number, data: SupplierUpdate): Promise<Supplier> =>
    apiClient.put<Supplier>(`/suppliers/${id}`, data),
};
