// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_order_history_status.html
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { StatusBadge } from '../components/StatusBadge';
import { Link } from 'react-router-dom';

export function OrderHistoryPage() {
  const orders = [
    {
      id: '#SS-2024-1234',
      date: 'March 15, 2024',
      total: 205.87,
      status: 'delivered',
      items: [
        { name: 'Wireless Bluetooth Headphones', brand: 'TechSound', quantity: 1, price: 89.99 },
        { name: 'Ergonomic Wireless Mouse', brand: 'ErgoTech', quantity: 2, price: 69.98 },
      ],
    },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <nav className="bg-white py-4 px-8 border-b border-gray-200">
        <div className="max-w-[1400px] mx-auto flex gap-8">
          {['My Orders', 'Profile', 'Addresses', 'Payment Methods', 'Wishlist'].map((tab, i) => (
            <Link
              key={tab}
              to={`/account/${tab.toLowerCase().replace(' ', '-')}`}
              className={`text-gray-700 no-underline font-medium px-4 py-2 rounded-md ${
                i === 0 ? 'bg-blue-50 text-blue-600 font-semibold' : 'hover:bg-gray-50'
              }`}
            >
              {tab}
            </Link>
          ))}
        </div>
      </nav>

      <main className="max-w-[1400px] mx-auto py-8 px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gray-900">My Orders</h1>
          <p className="text-gray-600">View and track your order history</p>
        </div>

        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.id} className="bg-white rounded-xl shadow-sm overflow-hidden">
              <div className="bg-gray-50 px-6 py-6 grid grid-cols-4 gap-4 border-b border-gray-200">
                <div>
                  <div className="text-xs text-gray-600 uppercase font-semibold mb-1">
                    Order Number
                  </div>
                  <div className="text-base font-semibold text-gray-900">{order.id}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 uppercase font-semibold mb-1">Order Date</div>
                  <div className="text-base font-semibold text-gray-900">{order.date}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 uppercase font-semibold mb-1">Total</div>
                  <div className="text-base font-semibold text-gray-900">${order.total.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 uppercase font-semibold mb-1">Status</div>
                  <StatusBadge status={order.status} />
                </div>
              </div>

              <div className="px-6 py-6">
                <div className="space-y-4 mb-6">
                  {order.items.map((item, i) => (
                    <div key={i} className="flex gap-4 items-center">
                      <div className="w-20 h-20 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg flex items-center justify-center text-3xl">
                        🎧
                      </div>
                      <div className="flex-1">
                        <div className="text-base font-semibold text-gray-900 mb-1">{item.name}</div>
                        <div className="text-sm text-gray-600">{item.brand}</div>
                        <div className="text-sm text-gray-700">Quantity: {item.quantity}</div>
                      </div>
                      <div className="text-lg font-bold text-blue-600">${item.price.toFixed(2)}</div>
                    </div>
                  ))}
                </div>

                <div className="pt-6 border-t border-gray-200">
                  <div className="text-base font-semibold mb-4 text-gray-900">
                    Order Status History
                  </div>
                  <div className="space-y-4">
                    {['Delivered', 'Out for Delivery', 'Shipped', 'Order Confirmed'].map((s, i) => (
                      <div key={i} className="flex gap-4 items-start">
                        <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center font-semibold text-sm">
                          ✓
                        </div>
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{s}</div>
                          <div className="text-sm text-gray-600">March {20 - i}, 2024</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex gap-4 pt-6 border-t border-gray-200 mt-6">
                  <button className="px-6 py-3 bg-blue-600 text-white border-none rounded-lg font-semibold cursor-pointer hover:bg-blue-700">
                    Buy Again
                  </button>
                  <button className="px-6 py-3 bg-white text-gray-700 border-2 border-gray-300 rounded-lg font-semibold cursor-pointer hover:bg-gray-50">
                    View Invoice
                  </button>
                  <button className="px-6 py-3 bg-white text-gray-700 border-2 border-gray-300 rounded-lg font-semibold cursor-pointer hover:bg-gray-50">
                    Contact Support
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
}
