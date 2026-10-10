// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_promotions_reviews_management.html
import { Link } from 'react-router-dom';

export function AdminReviewsPage() {
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
                i === 5 ? 'border-blue-600 text-white' : 'border-transparent hover:text-white hover:bg-white/5'
              }`}
            >
              {tab}
            </Link>
          ))}
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto py-8 px-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Review Moderation</h2>
          <button className="px-6 py-3 bg-blue-600 text-white border-none rounded-lg font-semibold cursor-pointer hover:bg-blue-700">
            View All Reviews
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <div className="text-lg font-semibold text-gray-900">Flagged Reviews</div>
            <input type="text" placeholder="Search reviews..." className="px-4 py-2 border border-gray-300 rounded-md text-sm w-64" />
          </div>
          <table className="w-full border-collapse">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Product</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Customer</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Rating</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Review</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Date</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Status</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-700 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  product: 'Wireless Bluetooth Headphones',
                  customer: 'Sarah Johnson',
                  rating: 5,
                  review: 'Absolutely love these headphones! The sound quality is incredible...',
                  date: 'Mar 15, 2024',
                  status: 'pending',
                },
                {
                  product: 'Ergonomic Wireless Mouse',
                  customer: 'Michael Chen',
                  rating: 5,
                  review: 'Great value for the price. Comfortable for long sessions...',
                  date: 'Mar 14, 2024',
                  status: 'approved',
                },
              ].map((review, i) => (
                <tr key={i} className="border-t border-gray-200 hover:bg-gray-50">
                  <td className="px-6 py-4">{review.product}</td>
                  <td className="px-6 py-4">{review.customer}</td>
                  <td className="px-6 py-4">
                    <span className="text-yellow-500">{'★'.repeat(review.rating)}</span>
                  </td>
                  <td className="px-6 py-4 max-w-md overflow-hidden text-ellipsis whitespace-nowrap">
                    {review.review}
                  </td>
                  <td className="px-6 py-4">{review.date}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-block px-3 py-1.5 rounded-xl text-xs font-semibold ${
                        review.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {review.status === 'pending' ? 'Pending' : 'Approved'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      <button className="px-3 py-1.5 bg-blue-600 text-white border-none rounded-md text-xs font-semibold cursor-pointer hover:bg-blue-700">
                        Approve
                      </button>
                      <button className="px-3 py-1.5 bg-red-600 text-white border-none rounded-md text-xs font-semibold cursor-pointer hover:bg-red-700">
                        Hide
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
