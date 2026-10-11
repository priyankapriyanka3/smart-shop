import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { catalogService } from '../../services/catalog';
import type { Product, Category } from '../../types/catalog';

export function HomePage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      catalogService.getCategories(),
      catalogService.getFeaturedProducts(4),
    ])
      .then(([categoriesResp, productsResp]) => {
        const cats = Array.isArray(categoriesResp) ? categoriesResp : categoriesResp.items || [];
        setCategories(cats.slice(0, 8));
        setFeaturedProducts(productsResp);
      })
      .catch((err) => console.error('Failed to load home data:', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Promotion Banner */}
      <div className="bg-[#FFF4E6] border border-[#FFD699] py-4 px-6 text-center text-[#B35900] font-medium">
        🎉 Limited Time Offer: Use code WELCOME20 for 20% off your first order!
      </div>

      {/* Hero Section */}
      <section
        className="text-white py-16 px-6 text-center"
        style={{
          background: 'linear-gradient(135deg, #0066FF 0%, #0052CC 100%)',
        }}
      >
        <div className="max-w-[800px] mx-auto">
          <h1 className="text-5xl font-bold mb-4">Discover Quality Products</h1>
          <p className="text-xl mb-8 opacity-95">
            Shop from our curated collection of 100+ premium products across 50 categories
          </p>
          <Link
            to="/products"
            className="inline-block bg-white text-[#0066FF] py-3.5 px-8 rounded-lg font-semibold text-base hover:bg-gray-50 transition-colors"
          >
            Start Shopping
          </Link>
        </div>
      </section>

      {/* Main Content */}
      <main className="max-w-[1440px] mx-auto py-12 px-6">
        {/* Categories Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-[#1A1A1A]">Shop by Category</h2>
          <div className="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-6">
            {categories.length > 0 ? (
              categories.map((category) => (
                <Link
                  key={category.id}
                  to={`/categories/${category.slug || category.id}`}
                  className="bg-white border border-[#E5E5E5] rounded-xl p-6 text-center hover:border-[#0066FF] hover:shadow-[0_4px_12px_rgba(0,102,255,0.1)] transition-all"
                >
                  <div className="text-5xl mb-3">
                    📦
                  </div>
                  <div className="text-base font-semibold mb-1 text-[#1A1A1A]">
                    {category.name}
                  </div>
                  <div className="text-sm text-[#666]">
                    View products
                  </div>
                </Link>
              ))
            ) : (
              <>
                <CategoryCard icon="📱" name="Electronics" count={24} />
                <CategoryCard icon="👕" name="Clothing" count={18} />
                <CategoryCard icon="🏠" name="Home & Garden" count={15} />
                <CategoryCard icon="📚" name="Books" count={12} />
                <CategoryCard icon="⚽" name="Sports" count={10} />
                <CategoryCard icon="🎮" name="Gaming" count={8} />
                <CategoryCard icon="💄" name="Beauty" count={7} />
                <CategoryCard icon="🍽️" name="Kitchen" count={6} />
              </>
            )}
          </div>
        </section>

        {/* Featured Products Section */}
        <section>
          <h2 className="text-3xl font-bold mb-8 text-[#1A1A1A]">Featured Products</h2>
          <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-6">
            {featuredProducts.length > 0 ? (
              featuredProducts.map((product) => (
                <Link
                  key={product.id}
                  to={`/products/${product.id}`}
                  className="bg-white border border-[#E5E5E5] rounded-xl overflow-hidden hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-shadow"
                >
                  <div className="w-full h-60 bg-[#F5F5F5] flex items-center justify-center text-6xl">
                    {product.image_url || '📦'}
                  </div>
                  <div className="p-4">
                    <div className="text-base font-semibold mb-2 text-[#1A1A1A]">
                      {product.name}
                    </div>
                    <div className="flex items-center gap-2 mb-2 text-sm">
                      <span className="text-[#FFB800]">★★★★★</span>
                      <span className="text-[#666]">(0 reviews)</span>
                    </div>
                    <div className="text-xl font-bold text-[#0066FF]">
                      ${product.price.toFixed(2)}
                    </div>
                    <div className="text-sm text-[#00A86B] mt-1">
                      {product.available_quantity && product.available_quantity > 0 ? 'In Stock' : 'Out of Stock'}
                    </div>
                  </div>
                </Link>
              ))
            ) : (
              <>
                <ProductCard
                  icon="📱"
                  name="Wireless Bluetooth Headphones"
                  rating={5}
                  reviews={127}
                  price={89.99}
                  availability="In Stock"
                />
                <ProductCard
                  icon="👕"
                  name="Premium Cotton T-Shirt"
                  rating={4}
                  reviews={89}
                  price={24.99}
                  availability="In Stock"
                />
                <ProductCard
                  icon="💻"
                  name="Ergonomic Wireless Mouse"
                  rating={5}
                  reviews={203}
                  price={34.99}
                  availability="Low Stock"
                />
                <ProductCard
                  icon="📚"
                  name="The Art of Programming"
                  rating={5}
                  reviews={156}
                  price={39.99}
                  availability="In Stock"
                />
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

function CategoryCard({ icon, name, count }: { icon: string; name: string; count: number }) {
  return (
    <Link
      to={`/categories/${name.toLowerCase().replace(/ & /g, '-').replace(/ /g, '-')}`}
      className="bg-white border border-[#E5E5E5] rounded-xl p-6 text-center hover:border-[#0066FF] hover:shadow-[0_4px_12px_rgba(0,102,255,0.1)] transition-all"
    >
      <div className="text-5xl mb-3">{icon}</div>
      <div className="text-base font-semibold mb-1 text-[#1A1A1A]">{name}</div>
      <div className="text-sm text-[#666]">{count} products</div>
    </Link>
  );
}

function ProductCard({
  icon,
  name,
  rating,
  reviews,
  price,
  availability,
}: {
  icon: string;
  name: string;
  rating: number;
  reviews: number;
  price: number;
  availability: string;
}) {
  const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
  const availabilityColor = availability === 'In Stock' ? '#00A86B' : '#FF8C00';

  return (
    <Link
      to="/products/1"
      className="bg-white border border-[#E5E5E5] rounded-xl overflow-hidden hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-shadow"
    >
      <div className="w-full h-60 bg-[#F5F5F5] flex items-center justify-center text-6xl">
        {icon}
      </div>
      <div className="p-4">
        <div className="text-base font-semibold mb-2 text-[#1A1A1A]">{name}</div>
        <div className="flex items-center gap-2 mb-2 text-sm">
          <span className="text-[#FFB800]">{stars}</span>
          <span className="text-[#666]">({reviews} reviews)</span>
        </div>
        <div className="text-xl font-bold text-[#0066FF]">${price.toFixed(2)}</div>
        <div className="text-sm mt-1" style={{ color: availabilityColor }}>
          {availability}
        </div>
      </div>
    </Link>
  );
}
