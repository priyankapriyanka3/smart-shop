/**
 * Tests for CartPage component
 * Covers quantity updates and item removal
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { CartPage } from '../src/pages/shopper/CartPage';
import { AuthProvider } from '../src/lib/auth-context';

describe('CartPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    // Set auth token for protected route
    localStorage.setItem('smart_shop_token', 'test-token');
  });

  const mockCartData = {
    id: 1,
    customer_id: 1,
    items: [
      {
        id: 1,
        product_id: 101,
        product_name: 'Wireless Headphones',
        product_brand: 'TechPro',
        quantity: 2,
        unit_price: 199.99,
        total_price: 399.98,
        availability: 'In Stock',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
      {
        id: 2,
        product_id: 102,
        product_name: 'Smart Watch',
        product_brand: 'TechPro',
        quantity: 1,
        unit_price: 299.99,
        total_price: 299.99,
        availability: 'In Stock',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    ],
    subtotal: 699.97,
    discount: 0,
    shipping: 0,
    tax: 0,
    total: 699.97,
    item_count: 3,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  const renderCartPage = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <CartPage />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('calls cart service when quantity is updated', async () => {
    const mockFetch = vi.fn()
      // Initial cart load
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockCartData,
      })
      // Update quantity response
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          ...mockCartData,
          items: [
            { ...mockCartData.items[0], quantity: 3, total_price: 599.97 },
            mockCartData.items[1],
          ],
        }),
      });
    global.fetch = mockFetch;

    renderCartPage();
    
    await waitFor(() => {
      expect(screen.getByText('Wireless Headphones')).toBeInTheDocument();
    }, { timeout: 3000 });

    // Find quantity inputs
    const quantityInputs = screen.getAllByRole('spinbutton');
    expect(quantityInputs.length).toBeGreaterThan(0);

    // Update quantity for first item
    fireEvent.change(quantityInputs[0], { target: { value: '3' } });
    
    await waitFor(() => {
      // Verify update was called
      const updateCalls = mockFetch.mock.calls.filter(call => 
        call[1]?.method === 'PATCH' || call[1]?.method === 'PUT'
      );
      expect(updateCalls.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });

  it('removes item from list when remove button is clicked', async () => {
    const mockFetch = vi.fn()
      // Initial cart load
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockCartData,
      })
      // Remove item response
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          ...mockCartData,
          items: [mockCartData.items[1]], // Only second item remains
        }),
      });
    global.fetch = mockFetch;

    renderCartPage();
    
    await waitFor(() => {
      expect(screen.getByText('Wireless Headphones')).toBeInTheDocument();
      expect(screen.getByText('Smart Watch')).toBeInTheDocument();
    }, { timeout: 3000 });

    // Find and click remove button
    const removeButtons = screen.getAllByRole('button', { name: /Remove/i });
    expect(removeButtons.length).toBeGreaterThan(0);
    
    fireEvent.click(removeButtons[0]);
    
    await waitFor(() => {
      // Verify delete was called
      const deleteCalls = mockFetch.mock.calls.filter(call => 
        call[1]?.method === 'DELETE'
      );
      expect(deleteCalls.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });
});
