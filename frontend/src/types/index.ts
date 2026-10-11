/**
 * Shared TypeScript types for Smart Shop
 */

export * from './auth';
export * from './catalog';
export * from './orders';
export * from './admin';

/**
 * Generic pagination wrapper matching backend response
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Generic API error response
 */
export interface ApiError {
  detail: string;
  status_code: number;
}
