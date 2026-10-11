/**
 * Tests for HomePage component
 * Covers category grid rendering and product grid rendering
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { HomePage } from '../src/pages/shopper/HomePage';
import { AuthProvider } from '../src/lib/auth-context';

describe('HomePage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  const renderHomePage = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <HomePage />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('renders hero section', async () => {
    // Mock fetch to return empty data
    const mockFetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ items: [], total: 0 }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ([]),
      });
    global.fetch = mockFetch;

    renderHomePage();
    
    await waitFor(() => {
      expect(screen.getByText(/Discover Quality Products/i)).toBeInTheDocument();
      expect(screen.getByText(/Start Shopping/i)).toBeInTheDocument();
    });
  });

  it('renders category grid when categories are loaded', async () => {
    const mockCategories = [
      { id: 1, name: 'Electronics', slug: 'electronics', description: 'Devices', parent_id: null, icon: '📱', product_count: 10 },
      { id: 2, name: 'Clothing', slug: 'clothing', description: 'Fashion', parent_id: null, icon: '👕', product_count: 20 },
      { id: 3, name: 'Home & Garden', slug: 'home-garden', description: 'Home items', parent_id: null, icon: '🏠', product_count: 15 },
      { id: 4, name: 'Sports', slug: 'sports', description: 'Fitness', parent_id: null, icon: '⚽', product_count: 12 },
    ];

    // Mock fetch for categories and products
    const mockFetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ items: mockCategories, total: 4 }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ items: [], total: 0 }),
      });
    global.fetch = mockFetch;

    renderHomePage();
    
    await waitFor(() => {
      expect(screen.getByText('Electronics')).toBeInTheDocument();
      expect(screen.getByText('Clothing')).toBeInTheDocument();
      expect(screen.getByText('Home & Garden')).toBeInTheDocument();
      expect(screen.getByText('Sports')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('renders product grid when featured products are loaded', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Wireless Headphones',
        slug: 'wireless-headphones',
        description: 'Premium audio',
        price: 99.99,
        sku: 'WH-001',
        category_id: 1,
        in_stock: true,
        stock_quantity: 50,
      },
      {
        id: 2,
        name: 'Smart Watch',
        slug: 'smart-watch',
        description: 'Track your fitness',
        price: 199.99,
        sku: 'SW-002',
        category_id: 1,
        in_stock: true,
        stock_quantity: 30,
      },
    ];

    // Mock fetch for categories and products
    const mockFetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ items: [], total: 0 }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ items: mockProducts, total: 2 }),
      });
    global.fetch = mockFetch;

    renderHomePage();
    
    await waitFor(() => {
      expect(screen.getByText('Wireless Headphones')).toBeInTheDocument();
      expect(screen.getByText('Smart Watch')).toBeInTheDocument();
    }, { timeout: 3000 });
  });
});
