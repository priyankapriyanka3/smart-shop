// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_category_listing.html
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { Breadcrumb } from '../components/Breadcrumb';
import { ProductCard } from '../components/ProductCard';

export function CategoryListingPage() {
  const products = Array(6).fill(null).map((_, i) => ({
    id: i + 1,
    name: i === 0 ? 'Wireless Bluetooth Headphones' : i === 1 ? 'Ergonomic Wireless Mouse' : `Product ${i}`,
    brand: i % 2 === 0 ? 'TechSound' : 'ErgoTech',
    price: (89.99 - i * 5).toFixed(2),
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

      <Breadcrumb items={[{ label: 'Home', path: '/' }, { label: 'Electronics' }]} />

      <div className="max-w-[1400px] mx-auto py-8 px-8 grid grid-cols-[280px_1fr] gap-8">
        <aside className="bg-white rounded-xl p-6 shadow-sm h-fit">
          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-gray-900">Price Range</div>
            <div className="flex gap-2 items-center">
              <input type="number" value="0" placeholder="Min" className="w-full px-2 py-2 border border-gray-300 rounded-md text-sm" />
              <span>-</span>
              <input type="number" value="500" placeholder="Max" className="w-full px-2 py-2 border border-gray-300 rounded-md text-sm" />
            </div>
          </div>
          
          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-gray-900">Brand</div>
            {['TechSound (12)', 'ErgoTech (8)', 'GameMaster (15)', 'BrightHome (6)'].map((brand, i) => (
              <div key={i} className="flex items-center gap-2 mb-3">
                <input type="checkbox" checked={i === 0} className="w-4.5 h-4.5 cursor-pointer" />
                <label className="text-sm text-gray-700 cursor-pointer">{brand}</label>
              </div>
            ))}
          </div>

          <button className="w-full py-3 bg-blue-600 text-white border-none rounded-lg font-semibold cursor-pointer hover:bg-blue-700">
            Apply Filters
          </button>
        </aside>

        <main>
          <div className="bg-white rounded-xl px-8 py-8 shadow-sm mb-8">
            <h1 className="text-4xl font-bold mb-2 text-gray-900">Electronics</h1>
            <p className="text-base text-gray-600">
              Discover the latest in technology, from headphones and accessories to smart home devices
              and gaming gear.
            </p>
          </div>

          <div className="bg-white rounded-xl px-6 py-6 shadow-sm mb-8 flex justify-between items-start">
            <div>
              <div className="text-sm text-gray-600 mb-2">Showing 24 of 156 products</div>
              <div className="flex gap-2 flex-wrap">
                {['TechSound', '4★ & Up', 'In Stock'].map((tag) => (
                  <span key={tag} className="bg-blue-50 text-blue-600 px-3 py-1.5 rounded-full text-sm flex items-center gap-2">
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
            {['Previous', '1', '2', '3', '4', 'Next'].map((btn) => (
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
