/**
 * Centralized API client for Smart Shop
 * Handles authentication, base URL, error handling, and 401 redirects
 */

import sharedConfig from '../../../shared_config.json';

// Determine base URL from environment or use relative /api
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Generic request function with auth header injection and error handling
 */
async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  // Get token from localStorage
  const token = localStorage.getItem(sharedConfig.auth.storage_key);
  
  // Build headers
  const headers = new Headers(options.headers);
  
  // Add auth header if token exists
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  
  // Add content-type for JSON payloads
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  
  // Make the request
  const url = `${BASE_URL}${sharedConfig.api_base_path}${path}`;
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  // Handle errors
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    const errorMessage = errorData.detail || 'Request failed';
    
    // Handle 401 - clear token and redirect to login
    if (response.status === 401) {
      localStorage.removeItem(sharedConfig.auth.storage_key);
      window.location.href = '/login';
    }
    
    throw new Error(errorMessage);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return null as T;
  }
  
  // Parse and return JSON
  return response.json() as Promise<T>;
}

/**
 * Exported API client with typed methods
 */
export const apiClient = {
  get: <T>(path: string) => request<T>(path, { method: 'GET' }),
  
  post: <T>(path: string, body?: unknown) => 
    request<T>(path, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    }),
  
  put: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    }),
  
  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
    }),
  
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
};

export default apiClient;
