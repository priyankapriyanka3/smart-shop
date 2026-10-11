/**
 * User/Customer types matching backend Pydantic models
 */

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string; // "shopper", "admin", "inventory_manager", "customer_support"
  is_active: string;
  created_at: string;
  updated_at: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface ProfileUpdate {
  full_name?: string;
  email?: string;
}
