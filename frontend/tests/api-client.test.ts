/**
 * Tests for API client
 * Covers 401 handling, token attachment, and request functionality
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { apiClient } from '../src/lib/api-client';

describe('API Client', () => {
  const originalLocation = window.location;
  
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    
    // Mock window.location for redirect tests
    delete (window as any).location;
    window.location = { ...originalLocation, href: '' } as Location;
  });

  afterEach(() => {
    window.location = originalLocation;
  });

  it('attaches Bearer token to authenticated requests', async () => {
    const mockToken = 'test-token-123';
    localStorage.setItem('smart_shop_token', mockToken);

    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.get('/test');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/test'),
      expect.objectContaining({
        headers: expect.any(Headers),
      })
    );

    // Check that Authorization header was set
    const callArgs = mockFetch.mock.calls[0];
    const headers = callArgs[1].headers as Headers;
    expect(headers.get('Authorization')).toBe(`Bearer ${mockToken}`);
  });

  it('makes requests without token when not authenticated', async () => {
    // No token in localStorage
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.get('/public');

    const callArgs = mockFetch.mock.calls[0];
    const headers = callArgs[1].headers as Headers;
    expect(headers.get('Authorization')).toBeNull();
  });

  it('clears token on 401 response', async () => {
    const mockToken = 'expired-token';
    localStorage.setItem('smart_shop_token', mockToken);

    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Unauthorized' }),
    });
    global.fetch = mockFetch;

    try {
      await apiClient.get('/protected');
    } catch (error) {
      // Expected to throw
    }

    // Token should be cleared from localStorage
    expect(localStorage.getItem('smart_shop_token')).toBeNull();
  });

  it('redirects to login on 401 response', async () => {
    localStorage.setItem('smart_shop_token', 'expired-token');

    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Unauthorized' }),
    });
    global.fetch = mockFetch;

    try {
      await apiClient.get('/protected');
    } catch (error) {
      // Expected to throw
    }

    // Should redirect to login
    expect(window.location.href).toBe('/login');
  });

  it('prepends api_base_path to all requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.get('/products');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/products'),
      expect.any(Object)
    );
  });

  it('includes Content-Type header for JSON payloads', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ success: true }),
    });
    global.fetch = mockFetch;

    await apiClient.post('/items', { name: 'Test Item' });

    const callArgs = mockFetch.mock.calls[0];
    const headers = callArgs[1].headers as Headers;
    expect(headers.get('Content-Type')).toBe('application/json');
  });

  it('serializes request body as JSON', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ success: true }),
    });
    global.fetch = mockFetch;

    const testData = { id: 1, name: 'Test' };
    await apiClient.post('/items', testData);

    const callArgs = mockFetch.mock.calls[0];
    const body = callArgs[1].body;
    expect(body).toBe(JSON.stringify(testData));
  });

  it('handles 204 No Content responses', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 204,
    });
    global.fetch = mockFetch;

    const result = await apiClient.delete('/items/1');

    expect(result).toBeNull();
  });

  it('throws error for non-OK responses', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Bad Request' }),
    });
    global.fetch = mockFetch;

    await expect(apiClient.get('/invalid')).rejects.toThrow('Bad Request');
  });

  it('handles network errors gracefully', async () => {
    const mockFetch = vi.fn().mockRejectedValue(new Error('Network error'));
    global.fetch = mockFetch;

    await expect(apiClient.get('/test')).rejects.toThrow('Network error');
  });

  it('supports GET requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.get('/test');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'GET' })
    );
  });

  it('supports POST requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ id: 1 }),
    });
    global.fetch = mockFetch;

    await apiClient.post('/items', { name: 'New Item' });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('supports PUT requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: 1, updated: true }),
    });
    global.fetch = mockFetch;

    await apiClient.put('/items/1', { name: 'Updated Item' });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'PUT' })
    );
  });

  it('supports PATCH requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: 1, patched: true }),
    });
    global.fetch = mockFetch;

    await apiClient.patch('/items/1', { status: 'active' });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'PATCH' })
    );
  });

  it('supports DELETE requests', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 204,
    });
    global.fetch = mockFetch;

    await apiClient.delete('/items/1');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'DELETE' })
    );
  });

  it('uses correct base URL from environment or config', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.get('/test');

    // Should use either VITE_API_URL or default to localhost:9000
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringMatching(/^http:\/\/localhost:9000\/api\/v1\/test/),
      expect.any(Object)
    );
  });

  it('handles error responses without JSON body', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: async () => {
        throw new Error('No JSON body');
      },
    });
    global.fetch = mockFetch;

    await expect(apiClient.get('/error')).rejects.toThrow();
  });

  it('does not redirect to login for non-401 errors', async () => {
    const originalHref = window.location.href;
    
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Server Error' }),
    });
    global.fetch = mockFetch;

    try {
      await apiClient.get('/error');
    } catch (error) {
      // Expected to throw
    }

    // Should NOT redirect on non-401 errors
    expect(window.location.href).toBe(originalHref);
  });

  it('preserves existing headers when adding auth', async () => {
    localStorage.setItem('smart_shop_token', 'test-token');

    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    await apiClient.post('/test', { data: 'test' });

    const callArgs = mockFetch.mock.calls[0];
    const headers = callArgs[1].headers as Headers;
    
    // Should have both Authorization and Content-Type
    expect(headers.get('Authorization')).toBeTruthy();
    expect(headers.get('Content-Type')).toBeTruthy();
  });
});
