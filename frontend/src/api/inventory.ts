/**
 * Inventory API endpoints
 */

import { apiClient } from './client';
import type { Inventory, InventoryUpdate, LowStockItem } from '../types/inventory';
import type { PaginatedResponse } from '../types/common';

export const inventoryApi = {
  /**
   * Get paginated inventory records (inventory_manager role)
   */
  getInventory: (params?: {
    page?: number;
    per_page?: number;
  }): Promise<PaginatedResponse<Inventory>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Inventory>>(`/inventory${query ? `?${query}` : ''}`);
  },

  /**
   * Update inventory quantity (inventory_manager role)
   */
  updateInventory: (id: number, data: InventoryUpdate): Promise<Inventory> =>
    apiClient.put<Inventory>(`/inventory/${id}`, data),

  /**
   * Get low-stock items (inventory_manager role)
   */
  getLowStockItems: (): Promise<LowStockItem[]> =>
    apiClient.get<LowStockItem[]>('/inventory/low-stock'),
};
