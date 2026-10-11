/**
 * Tests for LoginPage component
 * Covers form submission, validation, and auth context updates
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { LoginPage } from '../src/pages/shopper/LoginPage';
import { AuthProvider } from '../src/lib/auth-context';

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  const renderLoginPage = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('renders login and register forms', () => {
    renderLoginPage();
    
    // Use getAllBy since "Sign In" appears multiple times (heading and button)
    const signInElements = screen.getAllByText('Sign In');
    expect(signInElements.length).toBeGreaterThan(0);
    // "Create Account" also appears multiple times (heading and button)
    const createAccountElements = screen.getAllByText('Create Account');
    expect(createAccountElements.length).toBeGreaterThan(0);
  });

  it('pre-fills login form with default credentials (admin@example.com / admin123)', () => {
    renderLoginPage();
    
    const emailInputs = screen.getAllByLabelText(/Email Address/i);
    const passwordInputs = screen.getAllByLabelText(/Password/i);
    
    // Login form (first email/password inputs)
    expect(emailInputs[0]).toHaveValue('admin@example.com');
    expect(passwordInputs[0]).toHaveValue('admin123');
  });

  it('calls auth service and updates context on successful login', async () => {
    const mockLoginResponse = {
      access_token: 'test-token-123',
      token_type: 'bearer',
      user: {
        id: 1,
        email: 'admin@example.com',
        name: 'Admin User',
        role: 'admin',
        is_active: true,
      },
    };

    // Mock fetch to return successful login
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockLoginResponse,
    });
    global.fetch = mockFetch;

    renderLoginPage();
    
    const signInButtons = screen.getAllByRole('button', { name: /Sign In/i });
    
    // Submit form with pre-filled credentials
    fireEvent.click(signInButtons[0]);
    
    await waitFor(() => {
      // Verify auth service was called
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/auth/login'),
        expect.objectContaining({
          method: 'POST',
        })
      );
      
      // Verify token was stored (context updated)
      expect(localStorage.getItem('smart_shop_token')).toBe('test-token-123');
      
      // Verify navigation occurred
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  it('displays error message on login failure', async () => {
    // Mock failed login
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Invalid credentials' }),
    });
    global.fetch = mockFetch;

    renderLoginPage();
    
    const emailInputs = screen.getAllByLabelText(/Email Address/i);
    const passwordInputs = screen.getAllByLabelText(/Password/i);
    const signInButtons = screen.getAllByRole('button', { name: /Sign In/i });
    
    // Fill form with invalid credentials
    fireEvent.change(emailInputs[0], { target: { value: 'wrong@example.com' } });
    fireEvent.change(passwordInputs[0], { target: { value: 'wrongpass' } });
    
    // Submit form
    fireEvent.click(signInButtons[0]);
    
    await waitFor(() => {
      // Check that error message is displayed
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument();
    });
    
    // Verify token was NOT stored
    expect(localStorage.getItem('smart_shop_token')).toBeNull();
  });
});
