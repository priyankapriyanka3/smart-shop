/**
 * Authentication API endpoints
 */

import { apiClient } from './client';
import type { LoginRequest, LoginResponse, RegisterRequest, User, ProfileUpdate } from '../types/user';

export const authApi = {
  /**
   * Register a new customer account
   */
  register: (data: RegisterRequest): Promise<LoginResponse> =>
    apiClient.post<LoginResponse>('/auth/register', data),

  /**
   * Login with email and password
   */
  login: (data: LoginRequest): Promise<LoginResponse> =>
    apiClient.post<LoginResponse>('/auth/login', data),

  /**
   * Get current authenticated user profile
   */
  getProfile: (): Promise<User> =>
    apiClient.get<User>('/auth/me'),

  /**
   * Update current user profile
   */
  updateProfile: (data: ProfileUpdate): Promise<User> =>
    apiClient.put<User>('/auth/profile', data),
};
