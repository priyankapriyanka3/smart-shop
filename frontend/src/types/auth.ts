/**
 * Authentication and user types matching backend schemas
 */

/**
 * User data matching backend UserResponse schema
 */
export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

/**
 * Login request matching shared_config field names
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Login response matching backend LoginResponse schema
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/**
 * User registration request
 */
export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
}

/**
 * Address matching backend AddressResponse schema
 */
export interface Address {
  id: number;
  user_id: number;
  address_type: 'shipping' | 'billing';
  street: string;
  city: string;
  state_province: string;
  postal_code: string;
  country: string;
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Address creation request
 */
export interface AddressCreate {
  address_type: 'shipping' | 'billing';
  street: string;
  city: string;
  state_province: string;
  postal_code: string;
  country: string;
  is_default: boolean;
}
