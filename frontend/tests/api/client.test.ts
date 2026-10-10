/**
 * Tests for base API client
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { apiClient, ApiError } from '../../src/api/client';

describe('apiClient', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('request authentication', () => {
    it('should include Authorization header when token exists', async () => {
      localStorage.setItem('auth_token', 'test-token-123');
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve({ data: 'test' }),
        } as Response)
      );

      await apiClient.get('/test');

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/test'),
        expect.objectContaining({
          headers: expect.any(Headers),
        })
      );

      const callArgs = (fetch as any).mock.calls[0];
      const headers = callArgs[1].headers;
      expect(headers.get('Authorization')).toBe('Bearer test-token-123');
    });

    it('should not include Authorization header when no token exists', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve({ data: 'test' }),
        } as Response)
      );

      await apiClient.get('/test');

      const callArgs = (fetch as any).mock.calls[0];
      const headers = callArgs[1].headers;
      expect(headers.get('Authorization')).toBeNull();
    });
  });

  describe('error handling', () => {
    it('should throw ApiError on 401 and clear auth', async () => {
      localStorage.setItem('auth_token', 'test-token');
      localStorage.setItem('auth_user', JSON.stringify({ id: 1 }));

      const mockLocation = { href: '' };
      Object.defineProperty(window, 'location', {
        value: mockLocation,
        writable: true,
      });

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 401,
          json: () => Promise.resolve({ detail: 'Unauthorized' }),
        } as Response)
      );

      await expect(apiClient.get('/test')).rejects.toThrow(ApiError);
      expect(localStorage.getItem('auth_token')).toBeNull();
      expect(localStorage.getItem('auth_user')).toBeNull();
    });

    it('should throw ApiError with message on error response', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 400,
          json: () => Promise.resolve({ detail: 'Bad request' }),
        } as Response)
      );

      await expect(apiClient.get('/test')).rejects.toThrow('Bad request');
    });
  });

  describe('HTTP methods', () => {
    it('should make GET request', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve({ id: 1 }),
        } as Response)
      );

      const result = await apiClient.get('/test');
      expect(result).toEqual({ id: 1 });
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/test'),
        expect.objectContaining({ method: 'GET' })
      );
    });

    it('should make POST request with body', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          status: 201,
          json: () => Promise.resolve({ id: 1, name: 'test' }),
        } as Response)
      );

      const data = { name: 'test' };
      const result = await apiClient.post('/test', data);
      
      expect(result).toEqual({ id: 1, name: 'test' });
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/test'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(data),
        })
      );
    });

    it('should handle 204 No Content response', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          status: 204,
        } as Response)
      );

      const result = await apiClient.delete('/test/1');
      expect(result).toBeNull();
    });
  });
});
