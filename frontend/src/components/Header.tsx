import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';

export function Header() {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const cartCount = 3; // TODO: Get from cart context

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-[1400px] mx-auto px-8 py-4 flex items-center justify-between gap-8">
        <Link to="/" className="text-[1.75rem] font-bold text-blue-600 no-underline">
          Smart Shop
        </Link>

        <form onSubmit={handleSearch} className="flex-1 max-w-[600px]">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for products, brands, or categories..."
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
          />
        </form>

        <div className="flex gap-6 items-center">
          {isAuthenticated ? (
            <>
              <Link
                to="/account/orders"
                className="text-gray-700 no-underline font-medium hover:text-blue-600"
              >
                Account
              </Link>
              <Link
                to="/cart"
                className="text-gray-700 no-underline font-medium hover:text-blue-600 flex items-center gap-2"
              >
                Cart
                {cartCount > 0 && (
                  <span className="bg-red-600 text-white rounded-full w-5 h-5 inline-flex items-center justify-center text-xs font-semibold">
                    {cartCount}
                  </span>
                )}
              </Link>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-gray-700 no-underline font-medium hover:text-blue-600"
              >
                Sign In
              </Link>
              <Link
                to="/cart"
                className="text-gray-700 no-underline font-medium hover:text-blue-600"
              >
                Cart
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
