// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_search_filter_results.html
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { ProductCard } from '../components/ProductCard';
import { useState } from 'react';

export function SearchResultsPage() {
  const [filters, setFilters] = useState({
    categories: ['Electronics'],
    priceMin: '50',
    priceMax: '200',
    brands: ['TechSound', 'AudioPro'],
    rating: 5,
    inStock: true,
  });
  
  const products = Array(6).fill(null).map((_, i) => ({
    id: i + 1,
    name: 'Wireless Bluetooth Headphones',
    brand: 'TechSound',
    price: (89.99 + i * 10).toFixed(2),
    avg_rating: 4.8,
    review_count: 248,
    stock_status: 'in_stock' as const,
    sku: `TS-${i}`,
    description: 'Great product',
    is_active: "1",
    category_id: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }));

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <div className="bg-white py-4 px-8 border-b border-gray-200">
        <div className="max-w-[1400px] mx-auto flex justify-between items-center">
          <div className="text-lg text-gray-900">
            Search results for <strong className="text-blue-600">"wireless headphones"</strong>
          </div>
          <a href="/" className="text-red-600 no-underline font-medium text-sm hover:underline">
            Clear Search
          </a>
        </div>
      </div>

      <div className="max-w-[1400px] mx-auto py-8 px-8 grid grid-cols-[280px_1fr] gap-8">
        {/* Sidebar Filters */}
        <aside className="bg-white rounded-xl p-6 shadow-sm h-fit">
          <div className="flex justify-between items-center mb-6">
            <div className="text-lg font-semibold text-gray-900">Filters</div>
            <a href="#" className="text-blue-600 text-sm font-medium no-underline hover:underline">
              Clear All
            </a>
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-gray-900">Category</div>
            {['Electronics (18)', 'Audio (12)', 'Accessories (5)'].map((cat, i) => (
              <div key={i} className="flex items-center gap-2 mb-3">
                <input type="checkbox" checked={i === 0} className="w-4.5 h-4.5 cursor-pointer" />
                <label className="text-sm text-gray-700 cursor-pointer">{cat}</label>
              </div>
            ))}
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-gray-900">Price Range</div>
            <div className="flex gap-2 items-center">
              <input
                type="number"
                value={filters.priceMin}
                placeholder="Min"
                className="w-full px-2 py-2 border border-gray-300 rounded-md text-sm"
              />
              <span>-</span>
              <input
                type="number"
                value={filters.priceMax}
                placeholder="Max"
                className="w-full px-2 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-gray-900">Brand</div>
            {['TechSound (8)', 'AudioPro (6)', 'SoundMax (4)'].map((brand, i) => (
              <div key={i} className="flex items-center gap-2 mb-3">
                <input type="checkbox" checked={i < 2} className="w-4.5 h-4.5 cursor-pointer" />
                <label className="text-sm text-gray-700 cursor-pointer">{brand}</label>
              </div>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main>
          <div className="bg-white rounded-xl px-6 py-6 shadow-sm mb-8 flex justify-between items-center">
            <div>
              <div className="text-base font-semibold text-gray-900 mb-2">18 results found</div>
              <div className="flex gap-2 flex-wrap">
                {['Electronics', '$50 - $200', 'TechSound', 'AudioPro', '5★ & Up', 'In Stock'].map((tag) => (
                  <span
                    key={tag}
                    className="bg-blue-50 text-blue-600 px-3 py-1.5 rounded-full text-sm flex items-center gap-2"
                  >
                    {tag}
                    <span className="cursor-pointer font-bold">×</span>
                  </span>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-700">Sort by:</label>
              <select className="px-4 py-2 border border-gray-300 rounded-md text-sm cursor-pointer">
                <option>Relevance</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
                <option>Rating</option>
                <option>Newest</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-[repeat(auto-fill,minmax(260px,1fr))] gap-6 mb-8">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          <div className="flex justify-center gap-2">
            {['Previous', '1', '2', '3', 'Next'].map((btn) => (
              <button
                key={btn}
                className={`px-4 py-2 border border-gray-300 rounded-md text-sm cursor-pointer ${
                  btn === '1' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {btn}
              </button>
            ))}
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
