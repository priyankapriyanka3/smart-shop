// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_admin_inventory_orders_dashboard.html
import { Link } from 'react-router-dom';
import { StatusBadge } from '../components/StatusBadge';

export function AdminDashboardPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-gray-900 text-white py-4 px-8">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between">
          <div className="text-2xl font-bold">Smart Shop Admin</div>
          <div className="bg-blue-600 px-4 py-2 rounded-md font-semibold text-sm">Admin / Inventory Manager</div>
        </div>
      </header>

      <nav className="bg-gray-800 px-8">
        <div className="max-w-[1600px] mx-auto flex gap-2">
          {['Dashboard', 'Products', 'Orders', 'Inventory', 'Promotions', 'Reviews', 'Reports'].map((tab, i) => (
            <Link
              key={tab}
              to={`/admin/${tab.toLowerCase()}`}
              className={`text-white/70 no-underline px-6 py-4 font-medium border-b-[3px] ${
                i === 0 ? 'border-blue-600 text-white' : 'border-transparent hover:text-white hover:bg-white/5'
              }`}
            >
              {tab}
            </Link>
          ))}
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto py-8 px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gray-900">Dashboard Overview</h1>
          <p className="text-gray-600">Monitor orders, inventory, and key metrics</p>
        </div>

        <div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6 mb-8">
          {[
            { title: 'Pending Orders', value: '24', change: '↑ 12% from yesterday', icon: '📦', positive: true },
            { title: 'Low Stock Alerts', value: '8', change: '3 critical items', icon: '⚠️', warning: true },
            { title: "Today's Revenue", value: '$12,450', change: '↑ 8% from yesterday', icon: '💰', positive: true },
            { title: 'Active Products', value: '342', change: '↑ 5 new this week', icon: '📊', positive: true },
          ].map((card) => (
            <div key={card.title} className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <div className="text-sm text-gray-600 uppercase font-semibold">{card.title}</div>
                <div className="text-2xl">{card.icon}</div>
              </div>
              <div className="text-5xl font-bold text-gray-900 mb-2">{card.value}</div>
              <div className={`text-sm font-semibold ${card.positive ? 'text-green-600' : card.warning ? 'text-yellow-600' : 'text-gray-600'}`}>
                {card.change}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Recent Orders</h2>
          <button className="px-6 py-3 bg-blue-600 text-white border-none rounded-lg font-semibold cursor-pointer hover:bg-blue-700">
            View All Orders
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-8">
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <div className="text-lg font-semibold text-gray-900">Order Management</div>
            <input type="text" placeholder="Search orders..." className="px-4 py-2 border border-gray-300 rounded-md text-sm w-64" />
          </div>
          <table className="w-full border-collapse">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Order ID</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Customer</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Date</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Total</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Status</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {[
                { id: '#SS-2024-1234', customer: 'John Smith', date: 'March 15, 2024', total: 205.87, status: 'pending' },
                { id: '#SS-2024-1233', customer: 'Sarah Johnson', date: 'March 15, 2024', total: 149.99, status: 'confirmed' },
              ].map((order) => (
                <tr key={order.id} className="border-t border-gray-200 hover:bg-gray-50">
                  <td className="px-6 py-4">{order.id}</td>
                  <td className="px-6 py-4">{order.customer}</td>
                  <td className="px-6 py-4">{order.date}</td>
                  <td className="px-6 py-4">${order.total.toFixed(2)}</td>
                  <td className="px-6 py-4">
                    <StatusBadge status={order.status} />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      <button className="px-3 py-1.5 bg-blue-600 text-white border-none rounded-md text-xs font-semibold cursor-pointer hover:bg-blue-700">
                        Confirm
                      </button>
                      <button className="px-3 py-1.5 bg-white text-gray-700 border border-gray-300 rounded-md text-xs font-semibold cursor-pointer hover:bg-gray-50">
                        View
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
