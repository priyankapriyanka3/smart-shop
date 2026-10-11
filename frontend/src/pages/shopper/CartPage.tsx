import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { cartService } from '../../services/cart';
import type { Cart } from '../../types/cart';

export function CartPage() {
  const navigate = useNavigate();
  const [cart, setCart] = useState<Cart | null>(null);
  const [promoCode, setPromoCode] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cartService
      .getCart()
      .then(setCart)
      .catch((err) => console.error('Failed to load cart:', err))
      .finally(() => setLoading(false));
  }, []);

  const handleUpdateQuantity = async (itemId: number, quantity: number) => {
    try {
      const updatedCart = await cartService.updateItem(itemId, quantity);
      setCart(updatedCart);
    } catch (err) {
      console.error('Failed to update item:', err);
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      const updatedCart = await cartService.removeItem(itemId);
      setCart(updatedCart);
    } catch (err) {
      console.error('Failed to remove item:', err);
    }
  };

  const handleApplyPromo = async () => {
    try {
      const updatedCart = await cartService.applyPromoCode(promoCode);
      setCart(updatedCart);
    } catch (err) {
      console.error('Failed to apply promo:', err);
    }
  };

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!cart || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
          <Link to="/" className="text-[#0066FF] font-medium">Continue Shopping</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <div className="max-w-[1440px] mx-auto py-12 px-6">
        <h1 className="text-3xl font-bold mb-8">Shopping Cart ({cart.item_count} items)</h1>
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-8">
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            {cart.items.map((item, idx) => (
              <div key={item.id} className={`grid grid-cols-[120px_1fr_auto] gap-6 py-6 ${idx !== cart.items.length - 1 ? 'border-b border-[#E5E5E5]' : ''}`}>
                <div className="w-[120px] h-[120px] bg-[#F5F5F5] rounded-lg flex items-center justify-center text-5xl">🎧</div>
                <div className="flex flex-col justify-between">
                  <div>
                    <div className="text-lg font-semibold mb-2">{item.product_name}</div>
                    <div className="text-sm text-[#666] mb-2">{item.product_brand || 'TechPro'}</div>
                    <div className="text-sm text-[#00A86B] mb-4">✓ In Stock</div>
                  </div>
                  <div className="flex gap-4">
                    <div className="flex items-center gap-2">
                      <button onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)} className="w-8 h-8 border border-[#D1D1D1] bg-white rounded-md text-base">-</button>
                      <input type="number" value={item.quantity} onChange={(e) => handleUpdateQuantity(item.id, Number(e.target.value))} className="w-[60px] h-8 text-center border border-[#D1D1D1] rounded-md text-sm" min="1" />
                      <button onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)} className="w-8 h-8 border border-[#D1D1D1] bg-white rounded-md text-base">+</button>
                    </div>
                    <button onClick={() => handleRemoveItem(item.id)} className="text-[#DC2626] text-sm font-medium">Remove</button>
                  </div>
                </div>
                <div className="flex flex-col items-end justify-between">
                  <div className="text-xl font-bold text-[#0066FF]">${item.total_price.toFixed(2)}</div>
                  <div className="text-sm text-[#666]">${item.unit_price.toFixed(2)} each</div>
                </div>
              </div>
            ))}
            <div className="mt-6">
              <Link to="/" className="text-[#0066FF] font-medium">← Continue Shopping</Link>
            </div>
          </div>

          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6 h-fit sticky top-[100px]">
            <h2 className="text-xl font-bold mb-6">Order Summary</h2>
            <div className="mb-6 pb-6 border-b border-[#E5E5E5]">
              <div className="text-sm font-semibold mb-2">Promo Code</div>
              <div className="flex gap-2">
                <input type="text" value={promoCode} onChange={(e) => setPromoCode(e.target.value)} className="flex-1 py-2.5 px-2.5 border border-[#D1D1D1] rounded-md text-sm" placeholder="Enter code" />
                <button onClick={handleApplyPromo} className="py-2.5 px-5 bg-[#F5F5F5] border border-[#D1D1D1] rounded-md text-sm font-medium">Apply</button>
              </div>
            </div>
            <div className="flex justify-between mb-4 text-[15px]"><span className="text-[#666]">Subtotal ({cart.item_count} items)</span><span className="font-semibold">${cart.subtotal.toFixed(2)}</span></div>
            <div className="flex justify-between mb-4 text-[15px]"><span className="text-[#666]">Estimated Shipping</span><span className="font-semibold">${cart.shipping.toFixed(2)}</span></div>
            <div className="flex justify-between mb-4 text-[15px]"><span className="text-[#666]">Discount</span><span className="font-semibold text-[#00A86B]">-${cart.discount.toFixed(2)}</span></div>
            <div className="flex justify-between pt-6 mt-6 border-t-2 border-[#E5E5E5] text-xl font-bold"><span>Total</span><span>${cart.total.toFixed(2)}</span></div>
            <button onClick={() => navigate('/checkout')} className="w-full mt-6 py-4 bg-[#0066FF] text-white rounded-lg text-base font-semibold hover:bg-[#0052CC]">Proceed to Checkout</button>
            <div className="text-center text-sm text-[#666] mt-3">🔒 Secure Checkout</div>
          </div>
        </div>
      </div>
    </div>
  );
}
