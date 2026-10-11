/**
 * Tests for RequireAuth component
 * Covers authentication redirect behavior
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter, Routes, Route, MemoryRouter } from 'react-router-dom';
import { RequireAuth } from '../src/components/auth/RequireAuth';
import { AuthProvider } from '../src/lib/auth-context';

describe('RequireAuth', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  const ProtectedContent = () => <div>Protected Content</div>;
  const LoginPage = () => <div>Login Page</div>;

  it('redirects unauthenticated user to /login', async () => {
    // No token in localStorage (unauthenticated)
    
    render(
      <MemoryRouter initialEntries={['/protected']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/protected"
              element={
                <RequireAuth>
                  <ProtectedContent />
                </RequireAuth>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );
    
    // Should redirect to login page
    await waitFor(() => {
      expect(screen.getByText('Login Page')).toBeInTheDocument();
    });
    
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('renders protected content when user is authenticated', async () => {
    // Set token to simulate authenticated user
    localStorage.setItem('smart_shop_token', 'valid-token-123');
    
    render(
      <MemoryRouter initialEntries={['/protected']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/protected"
              element={
                <RequireAuth>
                  <ProtectedContent />
                </RequireAuth>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );
    
    // Should show protected content
    await waitFor(() => {
      expect(screen.getByText('Protected Content')).toBeInTheDocument();
    });
    
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });
});
