// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_cart.html
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { QuantityControl } from '../components/QuantityControl';

interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  product_brand: string;
  product_price: number;
  quantity: number;
  stock_status: string;
}

export function CartPage() {
  const [items, setItems] = useState<CartItem[]>([
    {
      id: 1,
      product_id: 1,
      product_name: 'Wireless Bluetooth Headphones',
      product_brand: 'TechSound',
      product_price: 89.99,
      quantity: 1,
      stock_status: 'in_stock',
    },
    {
      id: 2,
      product_id: 2,
      product_name: 'Ergonomic Wireless Mouse',
      product_brand: 'ErgoTech',
      product_price: 34.99,
      quantity: 2,
      stock_status: 'in_stock',
    },
  ]);

  const [discountCode, setDiscountCode] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState({ code: 'SAVE10', amount: 20.0 });

  const subtotal = items.reduce((sum, item) => sum + item.product_price * item.quantity, 0);
  const discountAmount = appliedDiscount ? appliedDiscount.amount : 0;
  const total = subtotal - discountAmount;

  const updateQuantity = (itemId: number, newQuantity: number) => {
    setItems(items.map((item) => (item.id === itemId ? { ...item, quantity: newQuantity } : item)));
  };

  const removeItem = (itemId: number) => {
    setItems(items.filter((item) => item.id !== itemId));
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <main className="max-w-[1400px] mx-auto py-8 px-8">
        <h1 className="text-4xl font-bold mb-8 text-gray-900">Shopping Cart</h1>

        <div className="grid grid-cols-[1fr_400px] gap-8">
          {/* Cart Items */}
          <div className="bg-white rounded-xl p-8 shadow-sm">
            {items.map((item) => (
              <div
                key={item.id}
                className="grid grid-cols-[120px_1fr_auto] gap-6 py-6 border-b border-gray-200 last:border-b-0"
              >
                <div className="w-30 h-30 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg flex items-center justify-center text-5xl">
                  🎧
                </div>
                <div className="flex flex-col gap-2">
                  <div className="text-lg font-semibold text-gray-900">{item.product_name}</div>
                  <div className="text-sm text-gray-600">{item.product_brand}</div>
                  <div className="text-xl font-bold text-blue-600">${item.product_price.toFixed(2)}</div>
                  <div className="text-sm text-green-700 font-medium">In Stock</div>
                </div>
                <div className="flex flex-col items-end gap-4">
                  <QuantityControl
                    value={item.quantity}
                    onChange={(qty) => updateQuantity(item.id, qty)}
                  />
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-red-600 text-sm font-medium cursor-pointer hover:underline bg-transparent border-none p-0"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}

            <Link to="/" className="inline-block text-blue-600 no-underline font-medium mt-6 hover:underline">
              ← Continue Shopping
            </Link>
          </div>

          {/* Order Summary */}
          <div className="bg-white rounded-xl p-8 shadow-sm h-fit">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">Order Summary</h2>

            <div className="mb-6 pb-6 border-b border-gray-200">
              <label className="block text-sm font-semibold text-gray-700 mb-2">Discount Code</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={discountCode}
                  onChange={(e) => setDiscountCode(e.target.value)}
                  placeholder="Enter code"
                  className="flex-1 px-3 py-3 border-2 border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600"
                />
                <button className="px-6 py-3 bg-gray-600 text-white border-none rounded-lg font-semibold cursor-pointer text-sm hover:bg-gray-700">
                  Apply
                </button>
              </div>
              {appliedDiscount && (
                <div className="mt-3 px-3 py-3 bg-green-100 rounded-md flex justify-between items-center">
                  <span className="font-semibold text-green-800 text-sm">{appliedDiscount.code} Applied</span>
                  <span
                    onClick={() => setAppliedDiscount(null as any)}
                    className="text-red-600 cursor-pointer text-sm"
                  >
                    ×
                  </span>
                </div>
              )}
            </div>

            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Subtotal ({items.length} items)</span>
              <span className="font-semibold text-gray-900">${subtotal.toFixed(2)}</span>
            </div>

            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Discount ({appliedDiscount?.code})</span>
              <span className="font-semibold text-green-600">-${discountAmount.toFixed(2)}</span>
            </div>

            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Shipping</span>
              <span className="font-semibold text-gray-900">Calculated at checkout</span>
            </div>

            <div className="flex justify-between pt-6 mt-6 border-t-2 border-gray-200 text-2xl font-bold">
              <span className="text-gray-900">Total</span>
              <span className="text-blue-600">${total.toFixed(2)}</span>
            </div>

            <Link to="/checkout">
              <button className="w-full py-4 bg-blue-600 text-white border-none rounded-lg text-lg font-semibold cursor-pointer mt-6 hover:bg-blue-700">
                Proceed to Checkout
              </button>
            </Link>

            <div className="text-center mt-4 text-sm text-gray-600">🔒 Secure Checkout</div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
