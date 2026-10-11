/**
 * Review API endpoints
 */

import { apiClient } from './client';
import type { Review, ReviewCreate, ReviewModerate } from '../types/review';
import type { PaginatedResponse } from '../types/common';

// Named exports for convenience
export const getProductReviews = (productId: number, params?: {
  page?: number;
  per_page?: number;
}): Promise<PaginatedResponse<Review>> => reviewsApi.getProductReviews(productId, params);

export const reviewsApi = {
  /**
   * Get reviews for a product
   */
  getProductReviews: (
    productId: number,
    params?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Review>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString());
    
    const query = searchParams.toString();
    return apiClient.get<PaginatedResponse<Review>>(
      `/products/${productId}/reviews${query ? `?${query}` : ''}`
    );
  },

  /**
   * Create a review (authenticated)
   */
  createReview: (data: ReviewCreate): Promise<Review> =>
    apiClient.post<Review>('/reviews', data),

  /**
   * Mark review as helpful
   */
  markHelpful: (reviewId: number): Promise<Review> =>
    apiClient.post<Review>(`/reviews/${reviewId}/helpful`),

  /**
   * Hide/show review (admin moderation)
   */
  moderateReview: (reviewId: number, data: ReviewModerate): Promise<Review> =>
    apiClient.patch<Review>(`/reviews/${reviewId}/hide`, data),
};
