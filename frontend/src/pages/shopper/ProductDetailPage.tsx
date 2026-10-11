import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { catalogService } from '../../services/catalog';
import { cartService } from '../../services/cart';
import type { Product } from '../../types/catalog';

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    if (id) {
      catalogService
        .getProductById(Number(id))
        .then(setProduct)
        .catch((err) => console.error('Failed to load product:', err))
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleAddToCart = async () => {
    if (!product) return;
    setAddingToCart(true);
    try {
      await cartService.addItem(product.id, quantity);
      alert('Added to cart!');
    } catch (err) {
      console.error('Failed to add to cart:', err);
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!product) return <div className="text-center py-12">Product not found</div>;

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <div className="max-w-[1440px] mx-auto py-4 px-6 text-sm text-[#666]">
        <Link to="/" className="text-[#0066FF]">Home</Link> / <Link to="/categories/electronics" className="text-[#0066FF]">Electronics</Link> / <span>{product.name}</span>
      </div>

      <div className="max-w-[1440px] mx-auto px-6 pb-12 grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
          <div className="w-full h-[500px] bg-[#F5F5F5] rounded-lg flex items-center justify-center text-[120px] mb-4">🎧</div>
          <div className="grid grid-cols-4 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className={`h-[100px] bg-[#F5F5F5] border-2 ${i === 1 ? 'border-[#0066FF]' : 'border-[#E5E5E5]'} rounded-lg flex items-center justify-center text-3xl`}>🎧</div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
          <div className="text-sm text-[#666] mb-2">{product.brand || 'TechPro'}</div>
          <h1 className="text-3xl font-bold mb-4 text-[#1A1A1A]">{product.name}</h1>
          <div className="flex items-center gap-4 mb-6 pb-6 border-b border-[#E5E5E5]">
            <div className="flex items-center gap-2 text-lg">
              <span className="text-[#FFB800]">★★★★★</span>
              <span className="font-semibold">4.8</span>
            </div>
            <a href="#reviews" className="text-[#0066FF] text-sm">127 reviews</a>
          </div>
          <div className="text-4xl font-bold text-[#0066FF] mb-4">${product.price.toFixed(2)}</div>
          <div className="text-sm text-[#666] mb-6">SKU: {product.sku || 'TP-WBH-001'}</div>
          <div className="bg-[#F0F9FF] border border-[#B3E0FF] rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2 font-semibold text-[#00A86B] mb-1">✓ In Stock</div>
            <div className="text-sm text-[#666]">Ships within 1-2 business days</div>
          </div>
          <div className="mb-8 pb-8 border-b border-[#E5E5E5]">
            <div className="text-lg font-semibold mb-3">Product Description</div>
            <div className="text-[#666] leading-relaxed">{product.description || 'Experience premium sound quality with our Wireless Bluetooth Headphones. Featuring advanced noise cancellation technology, 30-hour battery life, and comfortable over-ear design. Perfect for music lovers, commuters, and professionals who demand the best audio experience.'}</div>
          </div>
          <div className="mb-6">
            <div className="text-sm font-semibold mb-2">Quantity</div>
            <div className="flex items-center gap-3">
              <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="w-10 h-10 border border-[#D1D1D1] bg-white rounded-md text-lg">-</button>
              <input type="number" value={quantity} onChange={(e) => setQuantity(Number(e.target.value))} className="w-20 h-10 text-center border border-[#D1D1D1] rounded-md text-base" min="1" />
              <button onClick={() => setQuantity(quantity + 1)} className="w-10 h-10 border border-[#D1D1D1] bg-white rounded-md text-lg">+</button>
            </div>
          </div>
          <button onClick={handleAddToCart} disabled={addingToCart} className="w-full py-4 bg-[#0066FF] text-white rounded-lg text-base font-semibold mb-3 hover:bg-[#0052CC] disabled:opacity-50">{addingToCart ? 'Adding...' : 'Add to Cart'}</button>
          <button className="w-full py-4 bg-white text-[#1A1A1A] border border-[#D1D1D1] rounded-lg text-base font-semibold hover:bg-[#F5F5F5]">♡ Add to Wishlist</button>
        </div>
      </div>

      <div className="max-w-[1440px] mx-auto px-6 pb-12" id="reviews">
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
          <div className="flex justify-between items-center mb-8 pb-6 border-b border-[#E5E5E5]">
            <h2 className="text-2xl font-bold">Customer Reviews (127)</h2>
            <button className="py-3 px-6 bg-[#0066FF] text-white rounded-lg text-sm font-semibold">Write a Review</button>
          </div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="py-6 border-b border-[#E5E5E5]">
              <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-[#E5E5E5] rounded-full flex items-center justify-center text-xl">👤</div>
                  <div>
                    <div className="font-semibold mb-1">Sarah Johnson</div>
                    <div className="text-sm text-[#666]">January 15, 2026</div>
                  </div>
                </div>
                <div className="text-[#FFB800] text-base">★★★★★</div>
              </div>
              <div className="text-[#666] leading-relaxed mb-3">Absolutely love these headphones! The sound quality is exceptional and the noise cancellation works perfectly. Battery life is exactly as advertised. Highly recommend for anyone looking for premium wireless headphones.</div>
              <div className="text-sm text-[#666]">Was this helpful? <button className="text-[#0066FF] font-medium">Yes (24)</button> | <button className="text-[#0066FF] font-medium">No (2)</button></div>
            </div>
          ))}
        </div>
      </div>

      <div className="max-w-[1440px] mx-auto px-6 pb-12">
        <h2 className="text-2xl font-bold mb-6">Related Products</h2>
        <div className="grid grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <Link key={i} to={`/products/${i}`} className="bg-white border border-[#E5E5E5] rounded-xl overflow-hidden">
              <div className="w-full h-[200px] bg-[#F5F5F5] flex items-center justify-center text-5xl">🎧</div>
              <div className="p-4">
                <div className="text-sm font-semibold mb-2">Noise Cancelling Earbuds</div>
                <div className="text-lg font-bold text-[#0066FF]">$149.99</div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
