import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ordersService } from '../../services/orders';
import type { Order } from '../../types/orders';

export function OrderHistoryPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    ordersService
      .getOrders()
      .then((resp) => {
        const items = Array.isArray(resp) ? resp : resp.items || [];
        setOrders(items);
      })
      .catch((err) => console.error('Failed to load orders:', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <div className="max-w-[1440px] mx-auto py-12 px-6 grid grid-cols-[280px_1fr] gap-8">
        <aside className="bg-white border border-[#E5E5E5] rounded-xl p-6 h-fit sticky top-[100px]">
          <div className="pb-4 mb-4 border-b border-[#E5E5E5]">
            <div className="text-lg font-bold mb-1">John Smith</div>
            <div className="text-sm text-[#666]">john.smith@email.com</div>
          </div>
          <ul className="space-y-2">
            <li><Link to="/orders" className="block py-3 px-4 bg-[#F0F9FF] text-[#0066FF] rounded-md text-[15px] font-medium">📦 Orders</Link></li>
            <li><Link to="/account/profile" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">👤 Profile</Link></li>
            <li><Link to="/account/addresses" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">📍 Addresses</Link></li>
            <li><Link to="/account/payment-methods" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">💳 Payment Methods</Link></li>
            <li><Link to="/account/wishlist" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">❤️ Wishlist</Link></li>
            <li><Link to="/account/settings" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">⚙️ Settings</Link></li>
            <li><Link to="/logout" className="block py-3 px-4 text-[#1A1A1A] rounded-md text-[15px] font-medium hover:bg-[#F5F5F5]">🚪 Sign Out</Link></li>
          </ul>
        </aside>

        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
          <div className="flex justify-between items-center mb-8 pb-6 border-b border-[#E5E5E5]">
            <h1 className="text-3xl font-bold">Order History</h1>
            <select className="py-2.5 px-4 border border-[#D1D1D1] rounded-md text-sm">
              <option>All Orders</option>
              <option>Last 30 Days</option>
              <option>Last 6 Months</option>
              <option>2026</option>
              <option>2025</option>
            </select>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading orders...</div>
          ) : orders.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📦</div>
              <h3 className="text-xl font-bold mb-2">No orders yet</h3>
              <p className="text-[#666] mb-4">Start shopping to see your orders here</p>
              <Link to="/" className="text-[#0066FF] font-medium">Start Shopping</Link>
            </div>
          ) : (
            <>
              {[
                { id: '#SS-2026-001234', date: 'January 15, 2026', total: '$227.95', status: 'Delivered', statusClass: 'bg-[#D1FAE5] text-[#065F46]' },
                { id: '#SS-2026-001189', date: 'January 8, 2026', total: '$149.99', status: 'Shipped', statusClass: 'bg-[#DBEAFE] text-[#1E40AF]' },
                { id: '#SS-2025-009876', date: 'December 28, 2025', total: '$399.99', status: 'Delivered', statusClass: 'bg-[#D1FAE5] text-[#065F46]' },
              ].map((order, idx) => (
                <div key={idx} className="border border-[#E5E5E5] rounded-xl p-6 mb-6">
                  <div className="grid grid-cols-4 gap-4 pb-4 mb-4 border-b border-[#E5E5E5]">
                    <div><div className="text-sm text-[#666] mb-1">Order Number</div><div className="text-[15px] font-semibold">{order.id}</div></div>
                    <div><div className="text-sm text-[#666] mb-1">Order Date</div><div className="text-[15px] font-semibold">{order.date}</div></div>
                    <div><div className="text-sm text-[#666] mb-1">Total</div><div className="text-[15px] font-semibold">{order.total}</div></div>
                    <div><div className="text-sm text-[#666] mb-1">Status</div><div className="text-[15px] font-semibold"><span className={`inline-block py-1 px-3 rounded-xl text-sm font-semibold ${order.statusClass}`}>{order.status}</span></div></div>
                  </div>
                  <div className="space-y-4 mb-4">
                    {[1, 2].map((i) => (
                      <div key={i} className="flex gap-4">
                        <div className="w-20 h-20 bg-[#F5F5F5] rounded-lg flex items-center justify-center text-3xl">🎧</div>
                        <div className="flex-1">
                          <div className="text-base font-semibold mb-1">Wireless Bluetooth Headphones</div>
                          <div className="text-sm text-[#666] mb-1">TechPro</div>
                          <div className="text-sm text-[#666]">Quantity: 1</div>
                        </div>
                        <div className="text-base font-bold text-[#0066FF]">$89.99</div>
                      </div>
                    ))}
                  </div>
                  <div className="flex gap-3 pt-4 border-t border-[#E5E5E5]">
                    <button className="py-2.5 px-5 bg-[#0066FF] text-white border-[#0066FF] rounded-md text-sm font-medium">View Details</button>
                    {order.status === 'Delivered' ? (
                      <>
                        <button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium hover:bg-[#F5F5F5]">Track Package</button>
                        <button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium hover:bg-[#F5F5F5]">Buy Again</button>
                        <button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium hover:bg-[#F5F5F5]">Write Review</button>
                      </>
                    ) : (
                      <>
                        <button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium hover:bg-[#F5F5F5]">Track Package</button>
                        <button className="py-2.5 px-5 bg-white border border-[#D1D1D1] rounded-md text-sm font-medium hover:bg-[#F5F5F5]">Contact Support</button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
