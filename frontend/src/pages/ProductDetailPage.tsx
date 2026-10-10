// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_product_detail.html
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { Breadcrumb } from '../components/Breadcrumb';
import { QuantityControl } from '../components/QuantityControl';
import { getProduct } from '../api/products';
import { getProductReviews } from '../api/reviews';
import { Product } from '../types/product';
import { Review } from '../types/review';

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    Promise.all([
      getProduct(parseInt(id)),
      getProductReviews(parseInt(id), { page: 1, per_page: 3 }),
    ])
      .then(([productData, reviewsData]) => {
        setProduct(productData);
        const reviewItems = Array.isArray(reviewsData) ? reviewsData : reviewsData?.items || [];
        setReviews(reviewItems);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const renderStars = (rating: number) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const stars = [];
    for (let i = 0; i < fullStars; i++) stars.push('★');
    if (hasHalfStar && fullStars < 5) stars.push('☆');
    while (stars.length < 5) stars.push('☆');
    return stars.join('');
  };

  const getStockStatus = () => {
    if (!product) return { text: 'Loading...', color: 'text-gray-600', icon: '' };
    if (product.stock_status === 'in_stock') {
      return { text: 'In Stock - Ships within 2 business days', color: 'text-green-700', icon: '●' };
    } else if (product.stock_status === 'low_stock') {
      return { text: 'Low Stock - Order soon', color: 'text-yellow-700', icon: '●' };
    } else {
      return { text: 'Out of Stock', color: 'text-gray-700', icon: '●' };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-gray-600">Loading...</div>
        </main>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-red-600">Error: {error || 'Product not found'}</div>
        </main>
      </div>
    );
  }

  const stockStatus = getStockStatus();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <Breadcrumb
        items={[
          { label: 'Home', path: '/' },
          { label: 'Electronics', path: '/categories/1' },
          { label: 'Audio', path: '/categories/2' },
          { label: product.name },
        ]}
      />

      <main className="max-w-[1400px] mx-auto py-8 px-8">
        {/* Product Layout */}
        <div className="grid grid-cols-2 gap-12 bg-white rounded-xl p-8 shadow-sm mb-12">
          {/* Gallery */}
          <div className="flex flex-col gap-4">
            <div className="w-full h-[500px] bg-gradient-to-br from-gray-200 to-gray-300 rounded-xl flex items-center justify-center text-[8rem]">
              🎧
            </div>
            <div className="flex gap-4">
              {[0, 1, 2, 3].map((i) => (
                <div
                  key={i}
                  className={`w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg border-2 ${
                    i === 0 ? 'border-blue-600' : 'border-gray-300'
                  } cursor-pointer flex items-center justify-center text-3xl`}
                >
                  {i === 0 ? '🎧' : i === 1 ? '📦' : i === 2 ? '🔌' : '📱'}
                </div>
              ))}
            </div>
          </div>

          {/* Details */}
          <div className="flex flex-col gap-6">
            <h1 className="text-4xl font-bold text-gray-900">{product.name}</h1>

            <div className="flex gap-6 items-center">
              <span className="text-blue-600 font-semibold">{product.brand}</span>
              <span className="text-sm text-gray-600">SKU: {product.sku}</span>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-yellow-500 text-xl">{renderStars(product.avg_rating || 0)}</span>
              <span className="text-gray-700">{(product.avg_rating || 0).toFixed(1)} out of 5</span>
              <a href="#reviews" className="text-blue-600 no-underline hover:underline">
                ({product.review_count || 0} reviews)
              </a>
            </div>

            <div className="p-6 bg-gray-50 rounded-lg">
              <div className="text-4xl font-bold text-blue-600 mb-2">
                ${parseFloat(product.price as any).toFixed(2)}
              </div>
              <div className={`flex items-center gap-2 font-semibold ${stockStatus.color}`}>
                <span className="w-3 h-3 bg-green-600 rounded-full"></span>
                {stockStatus.text}
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">Description</h2>
              <p className="text-gray-700 leading-relaxed">{product.description}</p>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">Specifications</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex justify-between px-3 py-3 bg-gray-50 rounded-md">
                  <span className="font-semibold text-gray-700">Brand</span>
                  <span className="text-gray-900">{product.brand}</span>
                </div>
                <div className="flex justify-between px-3 py-3 bg-gray-50 rounded-md">
                  <span className="font-semibold text-gray-700">SKU</span>
                  <span className="text-gray-900">{product.sku}</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <span className="font-semibold text-gray-700">Quantity:</span>
              <QuantityControl value={quantity} onChange={setQuantity} max={10} />
            </div>

            <button className="w-full py-4 bg-blue-600 text-white border-none rounded-lg text-lg font-semibold cursor-pointer hover:bg-blue-700">
              Add to Cart
            </button>
          </div>
        </div>

        {/* Reviews Section */}
        <div className="bg-white rounded-xl p-8 shadow-sm mb-12" id="reviews">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-xl font-semibold text-gray-900">Customer Reviews</h2>
            <span className="text-gray-700">{product.review_count || 0} reviews</span>
          </div>

          <div className="space-y-4">
            {reviews.map((review) => (
              <div key={review.id} className="p-6 border border-gray-200 rounded-lg">
                <div className="flex justify-between items-center mb-3">
                  <div>
                    <div className="font-semibold text-gray-900">
                      {review.customer?.full_name || 'Anonymous'}
                    </div>
                    <span className="text-yellow-500">{renderStars(review.rating)}</span>
                  </div>
                  <span className="text-sm text-gray-600">
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-700 leading-relaxed mb-3">{review.review_text}</p>
                <div className="text-sm text-gray-600">Helpful ({review.helpful_count || 0})</div>
              </div>
            ))}
          </div>
        </div>

        {/* Related Products */}
        <div className="bg-white rounded-xl p-8 shadow-sm">
          <h2 className="text-xl font-semibold mb-6 text-gray-900">Related Products</h2>
          <div className="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="bg-gray-50 rounded-lg overflow-hidden cursor-pointer hover:shadow-md"
              >
                <div className="w-full h-44 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center text-5xl">
                  🎧
                </div>
                <div className="p-4">
                  <div className="text-sm font-semibold text-gray-900 mb-2">
                    Related Product {i}
                  </div>
                  <div className="text-xl font-bold text-blue-600">${(69.99 + i * 10).toFixed(2)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
