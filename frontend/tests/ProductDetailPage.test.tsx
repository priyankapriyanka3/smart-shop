/**
 * Tests for ProductDetailPage component
 * Covers add to cart functionality
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, Route, Routes, MemoryRouter } from 'react-router-dom';
import { ProductDetailPage } from '../src/pages/shopper/ProductDetailPage';
import { AuthProvider } from '../src/lib/auth-context';

describe('ProductDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  const mockProduct = {
    id: 1,
    category_id: 1,
    sku: 'WH-001',
    name: 'Wireless Headphones',
    slug: 'wireless-headphones',
    brand: 'TechBrand',
    description: 'Premium wireless headphones with noise cancellation',
    price: 199.99,
    image_url: 'headphones-1.jpg',
    status: 'active',
    available_quantity: 50,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  const renderProductDetailPage = () => {
    return render(
      <MemoryRouter initialEntries={['/products/1']}>
        <AuthProvider>
          <Routes>
            <Route path="/products/:id" element={<ProductDetailPage />} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );
  };

  it('calls cart service when add to cart button is clicked', async () => {
    // Set up auth token
    localStorage.setItem('smart_shop_token', 'test-token');

    const mockFetch = vi.fn()
      // First call: get product details
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockProduct,
      })
      // Second call: add to cart
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ message: 'Added to cart' }),
      });
    global.fetch = mockFetch;
    
    renderProductDetailPage();
    
    await waitFor(() => {
      // Product name appears in breadcrumb and heading, use getByRole for specificity
      expect(screen.getByRole('heading', { name: 'Wireless Headphones' })).toBeInTheDocument();
    }, { timeout: 3000 });

    const addToCartButton = screen.getByRole('button', { name: /Add to Cart/i });
    fireEvent.click(addToCartButton);
    
    await waitFor(() => {
      // Verify cart service was called
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/cart'),
        expect.objectContaining({
          method: 'POST',
        })
      );
    }, { timeout: 3000 });
  });
});
