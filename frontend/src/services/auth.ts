import { apiClient } from '../lib/api-client';
import type { LoginRequest, LoginResponse } from '../types/auth';

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    return apiClient.post<LoginResponse>('/auth/login', credentials);
  },

  async register(data: {
    name: string;
    email: string;
    password: string;
  }): Promise<LoginResponse> {
    return apiClient.post<LoginResponse>('/customers/register', data);
  },
};
