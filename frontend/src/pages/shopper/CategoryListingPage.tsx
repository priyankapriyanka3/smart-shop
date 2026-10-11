import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { catalogService } from '../../services/catalog';
import type { Product } from '../../types/catalog';

export function CategoryListingPage() {
  const { slug } = useParams<{ slug: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState({
    minPrice: 0,
    maxPrice: 500,
    brands: [] as string[],
    rating: null as number | null,
    inStock: true,
  });
  const [sortBy, setSortBy] = useState('relevance');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    catalogService
      .getProducts({
        sort_by: sortBy,
        min_price: filters.minPrice,
        max_price: filters.maxPrice,
        in_stock: filters.inStock,
        page,
        page_size: 8,
      })
      .then((resp) => {
        const items = Array.isArray(resp) ? resp : resp.items || [];
        setProducts(items);
        setTotal(Array.isArray(resp) ? resp.length : resp.total || 0);
      })
      .catch((err) => console.error('Failed to load products:', err))
      .finally(() => setLoading(false));
  }, [slug, sortBy, filters, page]);

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Breadcrumb */}
      <div className="max-w-[1440px] mx-auto py-4 px-6 text-sm text-[#666]">
        <Link to="/" className="text-[#0066FF]">
          Home
        </Link>{' '}
        / <span>{slug || 'Electronics'}</span>
      </div>

      {/* Main Layout */}
      <div className="max-w-[1440px] mx-auto px-6 pb-12 grid grid-cols-[280px_1fr] gap-8">
        {/* Sidebar Filters */}
        <aside className="bg-white border border-[#E5E5E5] rounded-xl p-6 h-fit sticky top-[100px]">
          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Price Range</div>
            <div className="flex gap-2 items-center">
              <input
                type="number"
                className="w-full py-2 px-2 border border-[#D1D1D1] rounded-md text-sm"
                placeholder="Min"
                value={filters.minPrice}
                onChange={(e) => setFilters({ ...filters, minPrice: Number(e.target.value) })}
              />
              <span>-</span>
              <input
                type="number"
                className="w-full py-2 px-2 border border-[#D1D1D1] rounded-md text-sm"
                placeholder="Max"
                value={filters.maxPrice}
                onChange={(e) => setFilters({ ...filters, maxPrice: Number(e.target.value) })}
              />
            </div>
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Brand</div>
            {['TechPro', 'SmartGear', 'AudioMax', 'VisionTech'].map((brand) => (
              <div key={brand} className="flex items-center gap-2 mb-3 text-sm">
                <input type="checkbox" className="w-[18px] h-[18px]" />
                <label>{brand}</label>
              </div>
            ))}
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Rating</div>
            <div className="flex items-center gap-2 mb-3 text-sm">
              <input type="checkbox" className="w-[18px] h-[18px]" />
              <label>★★★★★ (5)</label>
            </div>
            <div className="flex items-center gap-2 mb-3 text-sm">
              <input type="checkbox" className="w-[18px] h-[18px]" />
              <label>★★★★☆ & up (18)</label>
            </div>
            <div className="flex items-center gap-2 mb-3 text-sm">
              <input type="checkbox" className="w-[18px] h-[18px]" />
              <label>★★★☆☆ & up (24)</label>
            </div>
          </div>

          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Availability</div>
            <div className="flex items-center gap-2 mb-3 text-sm">
              <input
                type="checkbox"
                className="w-[18px] h-[18px]"
                checked={filters.inStock}
                onChange={(e) => setFilters({ ...filters, inStock: e.target.checked })}
              />
              <label>In Stock (20)</label>
            </div>
            <div className="flex items-center gap-2 mb-3 text-sm">
              <input type="checkbox" className="w-[18px] h-[18px]" />
              <label>Low Stock (4)</label>
            </div>
          </div>

          <button className="w-full py-2.5 bg-[#F5F5F5] border-0 rounded-md text-sm font-medium">
            Clear All Filters
          </button>
        </aside>

        {/* Content Area */}
        <div>
          {/* Category Header */}
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6 mb-6">
            <h1 className="text-3xl font-bold mb-2">{slug || 'Electronics'}</h1>
            <p className="text-[#666] text-[15px]">Discover the latest in technology and electronics</p>
          </div>

          {/* Controls Bar */}
          <div className="flex justify-between items-center mb-6 py-4 px-4 bg-white border border-[#E5E5E5] rounded-xl">
            <div className="text-[15px] text-[#666]">Showing {total} products</div>
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium">Sort by:</label>
              <select
                className="py-2 px-3 pr-8 border border-[#D1D1D1] rounded-md text-sm"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="relevance">Relevance</option>
                <option value="price_low">Price: Low to High</option>
                <option value="price_high">Price: High to Low</option>
                <option value="rating">Rating</option>
                <option value="newest">Newest</option>
              </select>
            </div>
          </div>

          {/* Product Grid */}
          {loading ? (
            <div className="text-center py-12">Loading products...</div>
          ) : (
            <>
              <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-6 mb-8">
                {products.map((product) => (
                  <Link
                    key={product.id}
                    to={`/products/${product.id}`}
                    className="bg-white border border-[#E5E5E5] rounded-xl overflow-hidden hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-shadow"
                  >
                    <div className="w-full h-60 bg-[#F5F5F5] flex items-center justify-center text-6xl">
                      {product.image_url || '📦'}
                    </div>
                    <div className="p-4">
                      <div className="text-sm text-[#666] mb-1">{product.brand || 'Brand'}</div>
                      <div className="text-base font-semibold mb-2 text-[#1A1A1A]">{product.name}</div>
                      <div className="flex items-center gap-2 mb-2 text-sm">
                        <span className="text-[#FFB800]">★★★★★</span>
                        <span className="text-[#666]">(0)</span>
                      </div>
                      <div className="text-xl font-bold text-[#0066FF]">${product.price.toFixed(2)}</div>
                      <div className={`text-sm mt-1 ${product.available_quantity && product.available_quantity > 0 ? 'text-[#00A86B]' : 'text-[#FF8C00]'}`}>
                        {product.available_quantity && product.available_quantity > 0 ? 'In Stock' : 'Low Stock'}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>

              {/* Pagination */}
              <div className="flex justify-center items-center gap-2 py-6">
                <button className="py-2 px-4 border border-[#D1D1D1] bg-white rounded-md text-sm font-medium">
                  Previous
                </button>
                <button className="py-2 px-4 bg-[#0066FF] text-white border-[#0066FF] rounded-md text-sm font-medium">
                  1
                </button>
                <button className="py-2 px-4 border border-[#D1D1D1] bg-white rounded-md text-sm font-medium">
                  2
                </button>
                <button className="py-2 px-4 border border-[#D1D1D1] bg-white rounded-md text-sm font-medium">
                  3
                </button>
                <button className="py-2 px-4 border border-[#D1D1D1] bg-white rounded-md text-sm font-medium">
                  Next
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
