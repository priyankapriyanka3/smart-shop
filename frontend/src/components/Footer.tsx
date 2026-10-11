import { Link } from 'react-router-dom';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-12 px-8 mt-16">
      <div className="max-w-[1400px] mx-auto grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-8">
        <div>
          <h3 className="text-white text-lg mb-4">Shop</h3>
          <Link to="/categories" className="text-gray-400 no-underline block mb-2 hover:text-white">
            All Categories
          </Link>
          <Link to="/new" className="text-gray-400 no-underline block mb-2 hover:text-white">
            New Arrivals
          </Link>
          <Link to="/best-sellers" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Best Sellers
          </Link>
          <Link to="/deals" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Deals
          </Link>
        </div>

        <div>
          <h3 className="text-white text-lg mb-4">Customer Service</h3>
          <Link to="/contact" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Contact Us
          </Link>
          <Link to="/shipping" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Shipping Info
          </Link>
          <Link to="/returns" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Returns
          </Link>
          <Link to="/faq" className="text-gray-400 no-underline block mb-2 hover:text-white">
            FAQ
          </Link>
        </div>

        <div>
          <h3 className="text-white text-lg mb-4">Account</h3>
          <Link to="/account/orders" className="text-gray-400 no-underline block mb-2 hover:text-white">
            My Orders
          </Link>
          <Link to="/account/profile" className="text-gray-400 no-underline block mb-2 hover:text-white">
            My Profile
          </Link>
          <Link to="/account/wishlist" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Wishlist
          </Link>
          <Link to="/account/reviews" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Reviews
          </Link>
        </div>

        <div>
          <h3 className="text-white text-lg mb-4">About</h3>
          <Link to="/about" className="text-gray-400 no-underline block mb-2 hover:text-white">
            About Us
          </Link>
          <Link to="/careers" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Careers
          </Link>
          <Link to="/privacy" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Privacy Policy
          </Link>
          <Link to="/terms" className="text-gray-400 no-underline block mb-2 hover:text-white">
            Terms of Service
          </Link>
        </div>
      </div>
    </footer>
  );
}
