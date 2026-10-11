/**
 * Admin Promotions & Reviews Management Page
 * Matches wireframe_admin_promotions_reviews_management.html exactly
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getPromotions, togglePromotionStatus } from '../../services/promotions';
import { getReviews, approveReview, rejectReview, ReviewWithDetails } from '../../services/reviews';
import { Promotion } from '../../types/admin';

export function AdminPromotionsReviewsPage() {
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [reviews, setReviews] = useState<ReviewWithDetails[]>([]);
  const [activeTab, setActiveTab] = useState<'pending' | 'approved' | 'rejected'>('pending');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [promotionsData, reviewsData] = await Promise.all([
        getPromotions({ page: 1, page_size: 10 }),
        getReviews({ page: 1, page_size: 10, status: activeTab }),
      ]);

      setPromotions(Array.isArray(promotionsData) ? promotionsData : promotionsData.items || []);
      setReviews(Array.isArray(reviewsData) ? reviewsData : reviewsData.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleApproveReview = async (reviewId: number) => {
    try {
      await approveReview(reviewId);
      loadData();
    } catch (err) {
      alert('Failed to approve review');
    }
  };

  const handleRejectReview = async (reviewId: number) => {
    try {
      await rejectReview(reviewId);
      loadData();
    } catch (err) {
      alert('Failed to reject review');
    }
  };

  const handleTogglePromotion = async (promotionId: number, currentStatus: boolean) => {
    try {
      await togglePromotionStatus(promotionId, !currentStatus);
      loadData();
    } catch (err) {
      alert('Failed to update promotion status');
    }
  };

  const getPromotionStatusBadge = (promotion: Promotion) => {
    const now = new Date();
    const startDate = new Date(promotion.start_date);
    const endDate = new Date(promotion.end_date);

    if (endDate < now) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#FEE2E2] text-[#991B1B]">
          Expired
        </span>
      );
    }

    if (startDate > now) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#FEF3C7] text-[#92400E]">
          Scheduled
        </span>
      );
    }

    if (promotion.is_active) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#D1FAE5] text-[#065F46]">
          Active
        </span>
      );
    }

    return (
      <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-800">
        Inactive
      </span>
    );
  };

  const getPromotionTypeBadge = (type: string) => {
    return (
      <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#E0E7FF] text-[#3730A3]">
        {type === 'percentage' ? 'Percentage' : type === 'fixed' ? 'Fixed Amount' : 'Free Shipping'}
      </span>
    );
  };

  const renderStars = (rating: number) => {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  };

  if (loading && promotions.length === 0) {
    return (
      <div className="min-h-screen bg-[#FAFAFA]">
        <AdminHeader />
        <div className="flex items-center justify-center h-96">
          <div className="text-gray-600">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Admin Header */}
      <AdminHeader />

      {/* Dashboard Container */}
      <div className="max-w-[1600px] mx-auto px-6 py-8">
        <h1 className="text-[28px] font-bold mb-6">Promotions & Reviews Management</h1>

        {/* Promotions Section */}
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8 mb-8">
          <div className="flex justify-between items-center pb-4 mb-6 border-b border-[#E5E5E5]">
            <h2 className="text-[22px] font-bold">Promotions</h2>
            <button className="px-5 py-2.5 bg-[#0066FF] text-white rounded-md text-sm font-semibold hover:bg-[#0052CC]">
              + Create Promotion
            </button>
          </div>

          <table className="w-full border-collapse">
            <thead className="bg-[#F5F5F5]">
              <tr>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Code</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Type</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Value</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Valid Period</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Usage</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Status</th>
                <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Actions</th>
              </tr>
            </thead>
            <tbody>
              {promotions.map((promo) => {
                const usagePercent = promo.max_uses ? (promo.usage_count / promo.max_uses) * 100 : 0;
                return (
                  <tr key={promo.id}>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      <span className="font-mono bg-[#F5F5F5] px-2 py-1 rounded font-semibold">
                        {promo.code}
                      </span>
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      {getPromotionTypeBadge(promo.discount_type)}
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      {promo.discount_type === 'percentage'
                        ? `${promo.discount_value}% off`
                        : promo.discount_type === 'fixed'
                        ? `$${promo.discount_value} off`
                        : '$0 shipping'}
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      {new Date(promo.start_date).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                      })}{' '}
                      -{' '}
                      {new Date(promo.end_date).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      <div className="w-full h-1.5 bg-[#E5E5E5] rounded-full overflow-hidden mb-1">
                        <div
                          className="h-full bg-[#0066FF]"
                          style={{ width: `${Math.min(usagePercent, 100)}%` }}
                        />
                      </div>
                      <div className="text-xs text-[#666]">
                        {promo.usage_count} / {promo.max_uses || '∞'} uses
                      </div>
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      {getPromotionStatusBadge(promo)}
                    </td>
                    <td className="px-3 py-4 border-b border-[#E5E5E5] text-sm">
                      <div className="flex gap-2">
                        <button className="px-3 py-1.5 bg-white border border-[#D1D1D1] rounded text-[13px] hover:bg-[#F5F5F5]">
                          Edit
                        </button>
                        <button
                          onClick={() => handleTogglePromotion(promo.id, promo.is_active)}
                          className="px-3 py-1.5 bg-white border border-[#DC2626] text-[#DC2626] rounded text-[13px] hover:bg-[#F5F5F5]"
                        >
                          {promo.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Reviews Section */}
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-8">
          <div className="flex justify-between items-center pb-4 mb-6 border-b border-[#E5E5E5]">
            <h2 className="text-[22px] font-bold">Reviews Moderation</h2>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 mb-6 border-b border-[#E5E5E5]">
            <button
              onClick={() => setActiveTab('pending')}
              className={`px-6 py-3 text-[15px] font-medium border-b-2 ${
                activeTab === 'pending'
                  ? 'text-[#0066FF] border-[#0066FF]'
                  : 'text-[#666] border-transparent'
              }`}
            >
              Pending (4)
            </button>
            <button
              onClick={() => setActiveTab('approved')}
              className={`px-6 py-3 text-[15px] font-medium border-b-2 ${
                activeTab === 'approved'
                  ? 'text-[#0066FF] border-[#0066FF]'
                  : 'text-[#666] border-transparent'
              }`}
            >
              Approved (127)
            </button>
            <button
              onClick={() => setActiveTab('rejected')}
              className={`px-6 py-3 text-[15px] font-medium border-b-2 ${
                activeTab === 'rejected'
                  ? 'text-[#0066FF] border-[#0066FF]'
                  : 'text-[#666] border-transparent'
              }`}
            >
              Rejected (8)
            </button>
          </div>

          {/* Review Cards */}
          {reviews.map((review) => (
            <div key={review.id} className="border border-[#E5E5E5] rounded-lg p-5 mb-4">
              <div className="flex justify-between items-start mb-4">
                <div className="flex gap-3">
                  <div className="w-[60px] h-[60px] bg-[#F5F5F5] rounded-md flex items-center justify-center text-2xl">
                    🎧
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold mb-1">
                      {review.product?.name || 'Product Name'}
                    </div>
                    <div className="text-[13px] text-[#666]">
                      {review.product?.brand || 'Brand'} • SKU: {review.product?.sku || 'SKU'}
                    </div>
                  </div>
                </div>
                <div className="text-[#FFB800] text-base">
                  {renderStars(review.rating)}
                </div>
              </div>

              <div className="mb-4">
                <div className="font-semibold mb-1">
                  {review.customer?.name || `Customer ${review.customer_id}`}
                </div>
                <div className="text-[13px] text-[#666] mb-3">
                  Submitted on{' '}
                  {new Date(review.created_at).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </div>
                <div className="text-[#666] leading-relaxed">
                  {review.review_text || 'No review text provided.'}
                </div>
              </div>

              {activeTab === 'pending' && (
                <div className="flex gap-3">
                  <button
                    onClick={() => handleApproveReview(review.id)}
                    className="px-5 py-2 bg-[#00A86B] text-white rounded-md text-sm font-medium"
                  >
                    ✓ Approve
                  </button>
                  <button
                    onClick={() => handleRejectReview(review.id)}
                    className="px-5 py-2 bg-white text-[#DC2626] border border-[#DC2626] rounded-md text-sm font-medium"
                  >
                    ✗ Reject
                  </button>
                </div>
              )}
            </div>
          ))}

          {reviews.length === 0 && (
            <div className="text-center py-8 text-[#666]">
              No {activeTab} reviews found.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/**
 * Admin Header Component (reused from AdminDashboardPage)
 */
function AdminHeader() {
  return (
    <header className="bg-[#1A1A1A] text-white px-6 py-4 sticky top-0 z-50">
      <div className="max-w-[1600px] mx-auto flex items-center justify-between">
        <div className="text-xl font-bold text-white">Smart Shop Admin</div>

        <nav className="flex gap-6">
          <Link
            to="/admin/dashboard"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Dashboard
          </Link>
          <Link
            to="/admin/catalog"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Catalog
          </Link>
          <Link
            to="/admin/inventory"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Inventory
          </Link>
          <Link
            to="/admin/orders"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Orders
          </Link>
          <Link
            to="/admin/promotions"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10 bg-[#0066FF]"
          >
            Promotions
          </Link>
          <Link
            to="/admin/reviews"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Reviews
          </Link>
          <Link
            to="/admin/support"
            className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10"
          >
            Support
          </Link>
        </nav>

        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-[#666] rounded-full flex items-center justify-center">
            👤
          </div>
          <span>Admin User</span>
        </div>
      </div>
    </header>
  );
}
