import { Link } from 'react-router-dom';
import { Product } from '../types/product';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const renderStars = (rating: number) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const stars = [];

    for (let i = 0; i < fullStars; i++) {
      stars.push('★');
    }
    if (hasHalfStar && fullStars < 5) {
      stars.push('☆');
    }
    while (stars.length < 5) {
      stars.push('☆');
    }

    return stars.join('');
  };

  const getStockBadge = () => {
    if (product.stock_status === 'in_stock') {
      return { text: 'In Stock', className: 'bg-green-100 text-green-800' };
    } else if (product.stock_status === 'low_stock') {
      return { text: 'Low Stock', className: 'bg-yellow-100 text-yellow-800' };
    } else {
      return { text: 'Out of Stock', className: 'bg-gray-100 text-gray-800' };
    }
  };

  const stockBadge = getStockBadge();

  return (
    <Link
      to={`/products/${product.id}`}
      className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 cursor-pointer no-underline block"
    >
      <div className="w-full h-60 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center text-6xl text-gray-400">
        📦
      </div>
      <div className="p-5">
        <div className="text-lg font-semibold text-gray-900 mb-2">{product.name}</div>
        <div className="text-sm text-gray-600 mb-3">{product.brand}</div>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-yellow-500 text-sm">{renderStars(product.avg_rating || 0)}</span>
          <span className="text-sm text-gray-600">({product.review_count || 0})</span>
        </div>
        <div className="flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-600">
            ${parseFloat(product.price as any).toFixed(2)}
          </div>
          <span className={`text-xs font-semibold px-3 py-1 rounded-xl ${stockBadge.className}`}>
            {stockBadge.text}
          </span>
        </div>
      </div>
    </Link>
  );
}
