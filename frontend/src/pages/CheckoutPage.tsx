// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_checkout_address_payment_review.html
import { useState } from 'react';
import { Link } from 'react-router-dom';

export function CheckoutPage() {
  const [step, setStep] = useState(2); // 1=Cart, 2=Delivery, 3=Payment, 4=Review
  const [firstName, setFirstName] = useState('John');
  const [lastName, setLastName] = useState('Smith');
  const [address, setAddress] = useState('123 Main Street');
  const [apartment, setApartment] = useState('');
  const [city, setCity] = useState('San Francisco');
  const [state, setState] = useState('CA');
  const [zipCode, setZipCode] = useState('94102');
  const [phone, setPhone] = useState('(555) 123-4567');
  const [paymentMethod, setPaymentMethod] = useState('credit');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 py-4 px-8">
        <div className="max-w-[1400px] mx-auto flex items-center justify-between">
          <Link to="/" className="text-[1.75rem] font-bold text-blue-600 no-underline">
            Smart Shop
          </Link>
          <div className="flex items-center gap-2 text-green-700 font-semibold">
            🔒 Secure Checkout
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="bg-white py-6 px-8 border-b border-gray-200">
        <div className="max-w-[1400px] mx-auto flex justify-between items-center">
          {[
            { num: '✓', label: 'Cart', active: false, completed: true },
            { num: '2', label: 'Delivery', active: step === 2, completed: step > 2 },
            { num: '3', label: 'Payment', active: step === 3, completed: step > 3 },
            { num: '4', label: 'Review', active: step === 4, completed: false },
          ].map((s, i) => (
            <div key={i} className="flex items-center gap-3 flex-1 relative">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm ${
                  s.completed
                    ? 'bg-green-600 text-white'
                    : s.active
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                }`}
              >
                {s.num}
              </div>
              <div
                className={`text-sm font-medium ${
                  s.active ? 'text-blue-600 font-semibold' : 'text-gray-600'
                }`}
              >
                {s.label}
              </div>
              {i < 3 && (
                <div
                  className={`absolute right-0 top-4 w-full h-0.5 ${
                    s.completed || s.active ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                  style={{ left: '50%', width: '100%' }}
                ></div>
              )}
            </div>
          ))}
        </div>
      </div>

      <main className="max-w-[1400px] mx-auto py-8 px-8">
        <div className="grid grid-cols-[1fr_400px] gap-8">
          <div className="bg-white rounded-xl p-8 shadow-sm">
            {/* Delivery Address */}
            <div className="mb-8 pb-8 border-b border-gray-200">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Delivery Address</h2>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">First Name</label>
                  <input
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">Last Name</label>
                  <input
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
              </div>
              <div className="flex flex-col gap-2 mb-4">
                <label className="text-sm font-semibold text-gray-700">Street Address</label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                />
              </div>
              <div className="flex flex-col gap-2 mb-4">
                <label className="text-sm font-semibold text-gray-700">
                  Apartment, Suite, etc. (Optional)
                </label>
                <input
                  type="text"
                  value={apartment}
                  onChange={(e) => setApartment(e.target.value)}
                  placeholder="Apt 4B"
                  className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">City</label>
                  <input
                    type="text"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">State</label>
                  <input
                    type="text"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
              </div>
            </div>

            {/* Payment Method */}
            <div className="mb-8 pb-8 border-b border-gray-200">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Payment Method</h2>
              <div className="flex gap-4 mb-6">
                {['credit', 'debit', 'wallet'].map((method) => (
                  <div
                    key={method}
                    onClick={() => setPaymentMethod(method)}
                    className={`flex-1 px-4 py-4 border-2 rounded-lg cursor-pointer text-center font-semibold ${
                      paymentMethod === method
                        ? 'border-blue-600 bg-blue-50 text-blue-600'
                        : 'border-gray-300 text-gray-700'
                    }`}
                  >
                    {method === 'credit' ? '💳 Credit Card' : method === 'debit' ? '🏦 Debit Card' : '📱 Digital Wallet'}
                  </div>
                ))}
              </div>
              <div className="flex flex-col gap-2 mb-4">
                <label className="text-sm font-semibold text-gray-700">Card Number</label>
                <input
                  type="text"
                  placeholder="1234 5678 9012 3456"
                  className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                />
              </div>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">Expiration Date</label>
                  <input
                    type="text"
                    placeholder="MM/YY"
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700">CVV</label>
                  <input
                    type="text"
                    placeholder="123"
                    className="px-3 py-3 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  />
                </div>
              </div>
            </div>

            {/* Order Review */}
            <div>
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Order Review</h2>
              <div className="flex justify-between mb-4 text-base">
                <span className="text-gray-700">Items (4)</span>
                <span className="font-semibold text-gray-900">$199.96</span>
              </div>
              <div className="flex justify-between mb-4 text-base">
                <span className="text-gray-700">Discount (SAVE10)</span>
                <span className="font-semibold text-green-600">-$20.00</span>
              </div>
              <div className="flex justify-between mb-4 text-base">
                <span className="text-gray-700">Shipping</span>
                <span className="font-semibold text-gray-900">$8.99</span>
              </div>
              <div className="flex justify-between mb-4 text-base">
                <span className="text-gray-700">Tax</span>
                <span className="font-semibold text-gray-900">$16.92</span>
              </div>
              <div className="flex justify-between pt-6 mt-6 border-t-2 border-gray-200 text-2xl font-bold">
                <span className="text-gray-900">Order Total</span>
                <span className="text-blue-600">$205.87</span>
              </div>
            </div>

            <div className="flex gap-4 mt-8">
              <Link to="/cart" className="flex-1">
                <button className="w-full py-4 bg-white text-gray-700 border-2 border-gray-300 rounded-lg text-base font-semibold cursor-pointer hover:bg-gray-50">
                  ← Back to Cart
                </button>
              </Link>
              <button className="flex-[2] py-4 bg-blue-600 text-white border-none rounded-lg text-base font-semibold cursor-pointer hover:bg-blue-700">
                Place Order
              </button>
            </div>

            <div className="text-center mt-4 text-sm text-gray-600">
              By placing your order, you agree to our Terms of Service and Privacy Policy. Your order
              will be processed securely.
            </div>
          </div>

          {/* Order Summary Sidebar */}
          <div className="bg-white rounded-xl p-8 shadow-sm h-fit">
            <h2 className="text-xl font-semibold mb-6 text-gray-900">Order Summary</h2>
            <div className="mb-6 pb-6 border-b border-gray-200">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex gap-4 mb-4">
                  <div className="w-15 h-15 bg-gradient-to-br from-gray-200 to-gray-300 rounded-md flex items-center justify-center text-2xl">
                    🎧
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-semibold text-gray-900 mb-1">Product {i}</div>
                    <div className="text-xs text-gray-600">Qty: 1</div>
                  </div>
                  <div className="font-semibold text-blue-600">$89.99</div>
                </div>
              ))}
            </div>

            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Subtotal</span>
              <span className="font-semibold text-gray-900">$199.96</span>
            </div>
            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Discount</span>
              <span className="font-semibold text-green-600">-$20.00</span>
            </div>
            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Shipping</span>
              <span className="font-semibold text-gray-900">$8.99</span>
            </div>
            <div className="flex justify-between mb-4 text-base">
              <span className="text-gray-700">Tax</span>
              <span className="font-semibold text-gray-900">$16.92</span>
            </div>
            <div className="flex justify-between pt-6 mt-6 border-t-2 border-gray-200 text-2xl font-bold">
              <span className="text-gray-900">Total</span>
              <span className="text-blue-600">$205.87</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
