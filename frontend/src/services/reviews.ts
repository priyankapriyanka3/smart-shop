/**
 * Reviews service for product review management and moderation
 */

import { apiClient } from '../lib/api-client';
import { Review, ReviewCreateRequest } from '../types/orders';
import { PaginatedResponse } from '../types/catalog';
import { Product } from '../types/catalog';
import { User } from '../types/auth';

/**
 * Review with product and customer details for display
 */
export interface ReviewWithDetails extends Review {
  product?: Product;
  customer?: User;
}

/**
 * Get reviews with pagination
 */
export async function getReviews(params?: {
  page?: number;
  page_size?: number;
  product_id?: number;
  status?: string;
}): Promise<PaginatedResponse<ReviewWithDetails>> {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set('page', params.page.toString());
  if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
  if (params?.product_id) searchParams.set('product_id', params.product_id.toString());
  if (params?.status) searchParams.set('status', params.status);
  
  const queryString = searchParams.toString();
  const url = `/reviews${queryString ? `?${queryString}` : ''}`;
  
  return apiClient.get<PaginatedResponse<ReviewWithDetails>>(url);
}

/**
 * Submit new review
 */
export async function submitReview(data: ReviewCreateRequest): Promise<Review> {
  return apiClient.post<Review>('/reviews', data);
}

/**
 * Approve review (admin only)
 */
export async function approveReview(reviewId: number): Promise<Review> {
  return apiClient.patch<Review>(`/admin/reviews/${reviewId}/approve`, {});
}

/**
 * Reject review (admin only)
 */
export async function rejectReview(reviewId: number): Promise<Review> {
  return apiClient.patch<Review>(`/admin/reviews/${reviewId}/reject`, {});
}

/**
 * Get review summary for a product
 */
export async function getReviewSummary(productId: number): Promise<{
  average_rating: number;
  total_reviews: number;
  rating_distribution: { [key: string]: number };
}> {
  return apiClient.get<{
    average_rating: number;
    total_reviews: number;
    rating_distribution: { [key: string]: number };
  }>(`/reviews/summary/${productId}`);
}
