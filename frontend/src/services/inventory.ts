/**
 * Inventory service for warehouse and stock management
 */

import { apiClient } from '../lib/api-client';
import { Inventory, Warehouse } from '../types/admin';
import { PaginatedResponse } from '../types/catalog';
import { Product } from '../types/catalog';

/**
 * Inventory with product details for display
 */
export interface InventoryWithProduct extends Inventory {
  product?: Product;
  warehouse?: Warehouse;
}

/**
 * Get inventory records with pagination
 */
export async function getInventory(params?: {
  page?: number;
  page_size?: number;
  status?: string;
}): Promise<PaginatedResponse<InventoryWithProduct>> {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set('page', params.page.toString());
  if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
  if (params?.status) searchParams.set('status', params.status);
  
  const queryString = searchParams.toString();
  const url = `/inventory${queryString ? `?${queryString}` : ''}`;
  
  return apiClient.get<PaginatedResponse<InventoryWithProduct>>(url);
}

/**
 * Get warehouses list
 */
export async function getWarehouses(): Promise<Warehouse[]> {
  const response = await apiClient.get<PaginatedResponse<Warehouse>>('/inventory/warehouses');
  return Array.isArray(response) ? response : response.items || [];
}

/**
 * Update inventory quantity
 */
export async function updateInventoryQuantity(
  inventoryId: number,
  quantity: number,
  reason?: string
): Promise<Inventory> {
  return apiClient.patch(`/inventory/${inventoryId}`, { quantity, reason });
}
