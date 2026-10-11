/**
 * Smart Shop Root Application Component
 * Wires React Router with AuthProvider and defines all application routes
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './lib/auth-context';
import { RequireAuth } from './components/auth/RequireAuth';

// Shopper pages
import { HomePage } from './pages/shopper/HomePage';
import { LoginPage } from './pages/shopper/LoginPage';
import { CategoryListingPage } from './pages/shopper/CategoryListingPage';
import { SearchResultsPage } from './pages/shopper/SearchResultsPage';
import { ProductDetailPage } from './pages/shopper/ProductDetailPage';
import { CartPage } from './pages/shopper/CartPage';
import { CheckoutPage } from './pages/shopper/CheckoutPage';
import { OrderHistoryPage } from './pages/shopper/OrderHistoryPage';

// Admin pages
import { AdminDashboardPage } from './pages/admin/AdminDashboardPage';
import { AdminPromotionsReviewsPage } from './pages/admin/AdminPromotionsReviewsPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public shopper routes - accessible without authentication */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/categories/:slug" element={<CategoryListingPage />} />
          <Route path="/search" element={<SearchResultsPage />} />
          
          {/* Protected shopper routes - require authentication */}
          <Route 
            path="/cart" 
            element={
              <RequireAuth>
                <CartPage />
              </RequireAuth>
            } 
          />
          <Route 
            path="/checkout" 
            element={
              <RequireAuth>
                <CheckoutPage />
              </RequireAuth>
            } 
          />
          <Route 
            path="/orders" 
            element={
              <RequireAuth>
                <OrderHistoryPage />
              </RequireAuth>
            } 
          />
          <Route 
            path="/orders/:id" 
            element={
              <RequireAuth>
                <OrderHistoryPage />
              </RequireAuth>
            } 
          />
          <Route 
            path="/account/*" 
            element={
              <RequireAuth>
                <OrderHistoryPage />
              </RequireAuth>
            } 
          />
          
          {/* Protected admin routes - require authentication and admin role */}
          <Route 
            path="/admin/*" 
            element={
              <RequireAuth requiredRole="admin">
                <Routes>
                  <Route path="/" element={<AdminDashboardPage />} />
                  <Route path="/dashboard" element={<AdminDashboardPage />} />
                  <Route path="/promotions" element={<AdminPromotionsReviewsPage />} />
                  <Route path="/reviews" element={<AdminPromotionsReviewsPage />} />
                </Routes>
              </RequireAuth>
            } 
          />
          
          {/* Catch-all fallback - redirect to home */}
          <Route path="*" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
