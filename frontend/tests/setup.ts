/**
 * Vitest test setup
 * Configures testing environment for React components
 */

import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend vitest's expect with jest-dom matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
  // Clear localStorage between tests
  localStorage.clear();
  // Clear sessionStorage between tests
  sessionStorage.clear();
  // Reset all mocks
  vi.clearAllMocks();
});

// Mock shared_config.json for tests
const mockSharedConfig = {
  api_base_path: '/api/v1',
  ports: {
    backend: 9000,
    frontend: 5173,
  },
  auth: {
    storage_key: 'smart_shop_token',
    login_request: {
      field_names: {
        username: 'email',
        password: 'password',
      },
    },
    login_response: {
      token_field: 'access_token',
      user_field: 'user',
    },
  },
};

// Mock the shared_config.json import
vi.mock('../shared_config.json', () => ({
  default: mockSharedConfig,
}));

// Mock window.matchMedia for responsive tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
