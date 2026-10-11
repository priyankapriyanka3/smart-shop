/**
 * Admin service for dashboard stats and administrative operations
 */

import { apiClient } from '../lib/api-client';
import { DashboardStats } from '../types/admin';

/**
 * Get dashboard statistics
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  return apiClient.get<DashboardStats>('/admin/stats');
}

/**
 * Update order status
 */
export async function updateOrderStatus(
  orderId: number,
  status: string
): Promise<void> {
  return apiClient.patch(`/admin/orders/${orderId}/status`, { status });
}
