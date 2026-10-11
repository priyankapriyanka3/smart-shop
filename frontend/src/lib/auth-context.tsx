/**
 * Authentication context provider for Smart Shop
 * Handles login, logout, token storage, and user state
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api-client';
import sharedConfig from '../../../shared_config.json';
import type { User, LoginRequest, LoginResponse } from '../types/auth';

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem(sharedConfig.auth.storage_key);
    if (token) {
      // Token exists, try to get user info from stored data or validate token
      // For now, we'll just mark as not loading
      // In a production app, you'd verify the token with the backend
      setIsLoading(false);
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
      
      // Extract token and user from response using shared_config field names
      const token = response[sharedConfig.auth.login_response.token_field as keyof LoginResponse] as string;
      const userData = response[sharedConfig.auth.login_response.user_field as keyof LoginResponse] as User;
      
      // Store token in localStorage
      localStorage.setItem(sharedConfig.auth.storage_key, token);
      
      // Update user state
      setUser(userData);
    } catch (error) {
      // Clear any stale data
      localStorage.removeItem(sharedConfig.auth.storage_key);
      setUser(null);
      throw error;
    }
  };

  const logout = () => {
    // Clear token from localStorage
    localStorage.removeItem(sharedConfig.auth.storage_key);
    
    // Clear user state
    setUser(null);
    
    // Redirect to login page
    window.location.href = '/login';
  };

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user || !!localStorage.getItem(sharedConfig.auth.storage_key),
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
