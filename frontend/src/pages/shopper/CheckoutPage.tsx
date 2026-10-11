import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export function CheckoutPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const handlePlaceOrder = async () => {
    setLoading(true);
    // Simulate order creation
    setTimeout(() => {
      alert('Order placed successfully!');
      navigate('/orders');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <header className="bg-white border-b border-[#E5E5E5] py-4 px-6">
        <div className="max-w-[1440px] mx-auto flex justify-center">
          <Link to="/" className="text-2xl font-bold text-[#0066FF]">Smart Shop</Link>
        </div>
      </header>

      <div className="max-w-[1440px] mx-auto py-8 px-6">
        <div className="flex justify-center items-center gap-4 mb-12">
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full ${step >= 1 ? 'bg-[#00A86B]' : 'bg-[#E5E5E5]'} text-white flex items-center justify-center text-sm font-semibold`}>{step > 1 ? '✓' : '1'}</div>
            <div className={`text-sm font-medium ${step === 1 ? 'text-[#0066FF]' : 'text-[#666]'}`}>Shipping</div>
          </div>
          <div className="text-[#D1D1D1] text-xl">→</div>
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full ${step >= 2 ? (step === 2 ? 'bg-[#0066FF]' : 'bg-[#00A86B]') : 'bg-[#E5E5E5]'} text-white flex items-center justify-center text-sm font-semibold`}>{step > 2 ? '✓' : '2'}</div>
            <div className={`text-sm font-medium ${step === 2 ? 'text-[#0066FF]' : 'text-[#666]'}`}>Payment</div>
          </div>
          <div className="text-[#D1D1D1] text-xl">→</div>
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full ${step === 3 ? 'bg-[#0066FF]' : 'bg-[#E5E5E5]'} text-white flex items-center justify-center text-sm font-semibold`}>3</div>
            <div className={`text-sm font-medium ${step === 3 ? 'text-[#0066FF]' : 'text-[#666]'}`}>Review</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-8">
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
            {step === 1 && (
              <div>
                <h2 className="text-xl font-bold mb-6 pb-4 border-b border-[#E5E5E5]">Shipping Address</h2>
                <div className="border-2 border-[#0066FF] bg-[#F0F9FF] rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-3 mb-2"><input type="radio" name="address" className="w-5 h-5" defaultChecked /><span className="font-semibold">Home Address</span></div>
                  <div className="ml-8 text-sm text-[#666]">John Smith<br />123 Main Street, Apt 4B<br />San Francisco, CA 94102<br />United States</div>
                </div>
                <div className="border-2 border-[#D1D1D1] rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-3 mb-2"><input type="radio" name="address" className="w-5 h-5" /><span className="font-semibold">Work Address</span></div>
                  <div className="ml-8 text-sm text-[#666]">John Smith<br />456 Business Ave, Suite 200<br />San Francisco, CA 94103<br />United States</div>
                </div>
                <div className="flex items-center gap-2 mb-4"><input type="checkbox" id="billing-same" className="w-[18px] h-[18px]" defaultChecked /><label htmlFor="billing-same" className="text-sm">Billing address same as shipping</label></div>
                <button onClick={() => setStep(2)} className="py-3 px-6 bg-[#0066FF] text-white rounded-lg font-semibold">Continue to Payment</button>
              </div>
            )}
            {step === 2 && (
              <div>
                <h2 className="text-xl font-bold mb-6 pb-4 border-b border-[#E5E5E5]">Payment Method</h2>
                <div className="grid gap-3 mb-6">
                  <div className="border-2 border-[#0066FF] bg-[#F0F9FF] rounded-lg p-4 flex items-center gap-3"><input type="radio" name="payment" className="w-5 h-5" defaultChecked /><span className="font-semibold">Credit / Debit Card</span><span className="ml-auto text-xl">💳</span></div>
                  <div className="border-2 border-[#D1D1D1] rounded-lg p-4 flex items-center gap-3"><input type="radio" name="payment" className="w-5 h-5" /><span className="font-semibold">PayPal</span><span className="ml-auto text-xl">🅿️</span></div>
                </div>
                <div className="mb-4"><label className="block text-sm font-semibold mb-2">Card Number</label><input type="text" className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px]" placeholder="1234 5678 9012 3456" /></div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div><label className="block text-sm font-semibold mb-2">Expiration Date</label><input type="text" className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px]" placeholder="MM/YY" /></div>
                  <div><label className="block text-sm font-semibold mb-2">CVV</label><input type="text" className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px]" placeholder="123" /></div>
                </div>
                <div className="mb-6"><label className="block text-sm font-semibold mb-2">Cardholder Name</label><input type="text" className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px]" placeholder="John Smith" /></div>
                <div className="bg-[#F5F5F5] rounded-lg p-4 mb-6">
                  <div className="text-sm font-semibold mb-2">Have a promo code?</div>
                  <div className="flex gap-2"><input type="text" className="flex-1 py-2.5 px-2.5 border border-[#D1D1D1] rounded-md text-sm" placeholder="Enter code" /><button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium">Apply</button></div>
                </div>
                <div className="flex gap-3">
                  <button onClick={() => setStep(1)} className="py-3 px-6 bg-white border border-[#D1D1D1] rounded-lg font-semibold">Back</button>
                  <button onClick={() => setStep(3)} className="py-3 px-6 bg-[#0066FF] text-white rounded-lg font-semibold">Review Order</button>
                </div>
              </div>
            )}
            {step === 3 && (
              <div>
                <h2 className="text-xl font-bold mb-6 pb-4 border-b border-[#E5E5E5]">Review Order</h2>
                <p className="text-[#666] mb-6">Please review your order details before placing your order.</p>
                <div className="flex gap-3">
                  <button onClick={() => setStep(2)} className="py-3 px-6 bg-white border border-[#D1D1D1] rounded-lg font-semibold">Back</button>
                  <button onClick={handlePlaceOrder} disabled={loading} className="py-3 px-6 bg-[#0066FF] text-white rounded-lg font-semibold disabled:opacity-50">{loading ? 'Placing Order...' : 'Place Order'}</button>
                </div>
              </div>
            )}
          </div>

          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6 h-fit sticky top-6">
            <h2 className="text-xl font-bold mb-6">Order Summary</h2>
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex gap-4 py-4 border-b border-[#E5E5E5]">
                <div className="w-[60px] h-[60px] bg-[#F5F5F5] rounded-md flex items-center justify-center text-2xl">🎧</div>
                <div className="flex-1"><div className="text-sm font-semibold mb-1">Wireless Bluetooth Headphones</div><div className="text-sm text-[#666]">Qty: 1</div></div>
                <div className="font-semibold text-[#0066FF]">$89.99</div>
              </div>
            ))}
            <div className="pt-4">
              <div className="flex justify-between mb-3 text-[15px]"><span className="text-[#666]">Subtotal</span><span className="font-semibold">$199.96</span></div>
              <div className="flex justify-between mb-3 text-[15px]"><span className="text-[#666]">Shipping</span><span className="font-semibold">$9.99</span></div>
              <div className="flex justify-between mb-3 text-[15px]"><span className="text-[#666]">Tax</span><span className="font-semibold">$18.00</span></div>
              <div className="flex justify-between mb-3 text-[15px]"><span className="text-[#666]">Discount</span><span className="font-semibold text-[#00A86B]">-$0.00</span></div>
              <div className="flex justify-between pt-4 mt-4 border-t-2 border-[#E5E5E5] text-xl font-bold"><span>Total</span><span>$227.95</span></div>
            </div>
            {step === 3 && <button onClick={handlePlaceOrder} disabled={loading} className="w-full mt-6 py-4 bg-[#0066FF] text-white rounded-lg text-base font-semibold hover:bg-[#0052CC] disabled:opacity-50">{loading ? 'Placing Order...' : 'Place Order'}</button>}
            <div className="text-center text-sm text-[#666] mt-3">🔒 Secure Checkout</div>
          </div>
        </div>
      </div>
    </div>
  );
}
