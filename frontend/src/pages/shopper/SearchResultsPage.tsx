import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { catalogService } from '../../services/catalog';
import type { Product } from '../../types/catalog';

export function SearchResultsPage() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (query) {
      setLoading(true);
      catalogService
        .searchProducts(query)
        .then((resp) => {
          const items = Array.isArray(resp) ? resp : resp.items || [];
          setProducts(items);
          setTotal(Array.isArray(resp) ? resp.length : resp.total || 0);
        })
        .catch((err) => console.error('Search failed:', err))
        .finally(() => setLoading(false));
    }
  }, [query]);

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <div className="max-w-[1440px] mx-auto px-6 pb-12 grid grid-cols-[280px_1fr] gap-8 pt-6">
        <aside className="bg-white border border-[#E5E5E5] rounded-xl p-6 h-fit sticky top-[100px]">
          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Price Range</div>
            <div className="flex gap-2 items-center">
              <input type="number" className="w-full py-2 px-2 border border-[#D1D1D1] rounded-md text-sm" placeholder="Min" defaultValue="0" />
              <span>-</span>
              <input type="number" className="w-full py-2 px-2 border border-[#D1D1D1] rounded-md text-sm" placeholder="Max" defaultValue="500" />
            </div>
          </div>
          <div className="mb-8">
            <div className="text-base font-semibold mb-4 text-[#1A1A1A]">Category</div>
            <div className="flex items-center gap-2 mb-3 text-sm"><input type="checkbox" className="w-[18px] h-[18px]" defaultChecked /><label>Electronics (8)</label></div>
            <div className="flex items-center gap-2 mb-3 text-sm"><input type="checkbox" className="w-[18px] h-[18px]" /><label>Audio (5)</label></div>
          </div>
          <button className="w-full py-2.5 bg-[#F5F5F5] rounded-md text-sm font-medium">Clear All Filters</button>
        </aside>

        <div>
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6 mb-6">
            <div className="text-sm text-[#666] mb-2">Search results for:</div>
            <h1 className="text-3xl font-bold mb-2">"{query}"</h1>
            <p className="text-[#666] text-[15px]">Found {total} products matching your search</p>
          </div>

          <div className="flex justify-between items-center mb-6 py-4 px-4 bg-white border border-[#E5E5E5] rounded-xl">
            <div className="text-[15px] text-[#666]">Showing {total} products</div>
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium">Sort by:</label>
              <select className="py-2 px-3 border border-[#D1D1D1] rounded-md text-sm">
                <option>Relevance</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
                <option>Rating</option>
                <option>Newest</option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-12">Searching...</div>
          ) : products.length === 0 ? (
            <div className="text-center py-12 bg-white border border-[#E5E5E5] rounded-xl p-8">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-bold mb-2">No results found</h3>
              <p className="text-[#666] mb-4">Try adjusting your search or filters</p>
            </div>
          ) : (
            <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-6">
              {products.map((product) => (
                <Link key={product.id} to={`/products/${product.id}`} className="bg-white border border-[#E5E5E5] rounded-xl overflow-hidden hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)]">
                  <div className="w-full h-60 bg-[#F5F5F5] flex items-center justify-center text-6xl">{product.image_url || '📦'}</div>
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
          )}
        </div>
      </div>
    </div>
  );
}
