/**
 * Header component for Smart Shop
 * Includes logo, navigation, search, and user controls
 */

import { Link } from 'react-router-dom';
import { useAuth } from '../../lib/auth-context';

export function Header() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">Smart Shop</span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">
              Home
            </Link>
            <Link to="/categories" className="text-gray-700 hover:text-blue-600 font-medium">
              Categories
            </Link>
            <Link to="/search" className="text-gray-700 hover:text-blue-600 font-medium">
              Search
            </Link>
          </nav>

          {/* User controls */}
          <div className="flex items-center space-x-4">
            {/* Search icon */}
            <Link
              to="/search"
              className="text-gray-600 hover:text-blue-600"
              aria-label="Search"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </Link>

            {/* Cart */}
            {isAuthenticated && (
              <Link
                to="/cart"
                className="relative text-gray-600 hover:text-blue-600"
                aria-label="Shopping cart"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </Link>
            )}

            {/* User menu */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link
                  to="/orders"
                  className="text-gray-700 hover:text-blue-600 font-medium"
                >
                  Orders
                </Link>
                {user?.role === 'admin' && (
                  <Link
                    to="/admin/dashboard"
                    className="text-gray-700 hover:text-blue-600 font-medium"
                  >
                    Admin
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="text-gray-700 hover:text-blue-600 font-medium"
                >
                  Logout
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
