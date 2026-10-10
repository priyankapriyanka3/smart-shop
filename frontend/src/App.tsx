import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { RequireAuth } from './components/RequireAuth';
import { HomePage } from './pages/HomePage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { LoginPage } from './pages/LoginPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { OrderHistoryPage } from './pages/OrderHistoryPage';
import { SearchResultsPage } from './pages/SearchResultsPage';
import { CategoryListingPage } from './pages/CategoryListingPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AdminPromotionsPage } from './pages/AdminPromotionsPage';
import { AdminReviewsPage } from './pages/AdminReviewsPage';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/search" element={<SearchResultsPage />} />
          <Route path="/categories/:id" element={<CategoryListingPage />} />
          <Route path="/categories" element={<CategoryListingPage />} />

          {/* Protected Customer Routes */}
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
            path="/account/orders"
            element={
              <RequireAuth>
                <OrderHistoryPage />
              </RequireAuth>
            }
          />

          {/* Admin Routes */}
          <Route
            path="/admin/dashboard"
            element={
              <RequireAuth requiredRole="admin">
                <AdminDashboardPage />
              </RequireAuth>
            }
          />
          <Route
            path="/admin/promotions"
            element={
              <RequireAuth requiredRole="admin">
                <AdminPromotionsPage />
              </RequireAuth>
            }
          />
          <Route
            path="/admin/reviews"
            element={
              <RequireAuth requiredRole="admin">
                <AdminReviewsPage />
              </RequireAuth>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
