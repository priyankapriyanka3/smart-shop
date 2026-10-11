// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_promotions_reviews_management.html
import { Link } from 'react-router-dom';

export function AdminPromotionsPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-gray-900 text-white py-4 px-8">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between">
          <div className="text-2xl font-bold">Smart Shop Admin</div>
          <div className="bg-blue-600 px-4 py-2 rounded-md font-semibold text-sm">Admin</div>
        </div>
      </header>

      <nav className="bg-gray-800 px-8">
        <div className="max-w-[1600px] mx-auto flex gap-2">
          {['Dashboard', 'Products', 'Orders', 'Inventory', 'Promotions', 'Reviews', 'Reports'].map((tab, i) => (
            <Link
              key={tab}
              to={`/admin/${tab.toLowerCase()}`}
              className={`text-white/70 no-underline px-6 py-4 font-medium border-b-[3px] ${
                i === 4 ? 'border-blue-600 text-white' : 'border-transparent hover:text-white hover:bg-white/5'
              }`}
            >
              {tab}
            </Link>
          ))}
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto py-8 px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gray-900">Promotions & Reviews Management</h1>
          <p className="text-gray-600">Manage discount codes and moderate customer reviews</p>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Active Promotions</h2>
          <button className="px-6 py-3 bg-blue-600 text-white border-none rounded-lg font-semibold cursor-pointer hover:bg-blue-700">
            Create New Discount
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-8">
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <div className="text-lg font-semibold text-gray-900">Discount Codes</div>
            <input type="text" placeholder="Search discounts..." className="px-4 py-2 border border-gray-300 rounded-md text-sm w-64" />
          </div>
          <table className="w-full border-collapse">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Code</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Discount</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Valid Period</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Usage</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Status</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {[
                { code: 'SAVE10', discount: '10% off', period: 'Mar 1 - Mar 31, 2024', used: 248, max: 500, status: 'active' },
                { code: 'WELCOME20', discount: '$20 off', period: 'Jan 1 - Dec 31, 2024', used: 892, max: 1000, status: 'active' },
              ].map((promo) => (
                <tr key={promo.code} className="border-t border-gray-200 hover:bg-gray-50">
                  <td className="px-6 py-4"><strong>{promo.code}</strong></td>
                  <td className="px-6 py-4">{promo.discount}</td>
                  <td className="px-6 py-4">{promo.period}</td>
                  <td className="px-6 py-4">
                    <div>{promo.used} / {promo.max}</div>
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-600" style={{ width: `${(promo.used / promo.max) * 100}%` }}></div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-block px-3 py-1.5 rounded-xl text-xs font-semibold bg-green-100 text-green-800">Active</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      <button className="px-3 py-1.5 bg-white text-gray-700 border border-gray-300 rounded-md text-xs font-semibold cursor-pointer hover:bg-gray-50">
                        Edit
                      </button>
                      <button className="px-3 py-1.5 bg-red-600 text-white border-none rounded-md text-xs font-semibold cursor-pointer hover:bg-red-700">
                        Deactivate
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
