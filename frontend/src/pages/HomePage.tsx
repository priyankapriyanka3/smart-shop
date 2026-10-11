// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_home_catalog.html
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { ProductCard } from '../components/ProductCard';
import { getProducts } from '../api/products';
import { getCategories } from '../api/categories';
import { Product } from '../types/product';
import { Category } from '../types/category';

export function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      getProducts({ page: 1, per_page: 8 }),
      getCategories(),
    ])
      .then(([productsData, categoriesData]) => {
        const items = Array.isArray(productsData) ? productsData : (productsData as any)?.items || [];
        setProducts(items);
        const cats = Array.isArray(categoriesData) ? categoriesData : (categoriesData as any)?.items || [];
        setCategories(cats);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-gray-600">Loading...</div>
        </main>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-red-600">Error: {error}</div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-purple-600 to-purple-800 text-white py-16 px-8 text-center">
        <div className="max-w-[1400px] mx-auto">
          <h1 className="text-5xl font-bold mb-4">Discover Your Perfect Products</h1>
          <p className="text-xl opacity-95 mb-8">
            Browse thousands of quality items with fast delivery and trusted reviews
          </p>
          <Link
            to="/categories"
            className="inline-block bg-white text-purple-600 px-10 py-4 no-underline rounded-lg text-lg font-semibold hover:bg-gray-50"
          >
            Shop Now
          </Link>
        </div>
      </section>

      {/* Categories Navigation */}
      <nav className="bg-white border-b border-gray-200 py-4 px-8">
        <div className="max-w-[1400px] mx-auto flex gap-8 overflow-x-auto">
          {categories.slice(0, 7).map((category) => (
            <Link
              key={category.id}
              to={`/categories/${category.id}`}
              className="text-gray-700 no-underline font-medium whitespace-nowrap px-4 py-2 rounded-md hover:bg-gray-50 hover:text-blue-600"
            >
              {category.name}
            </Link>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-[1400px] mx-auto py-12 px-8">
        <h2 className="text-3xl font-bold mb-8 text-gray-900">Featured Products</h2>

        <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-8 mb-16">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
}
