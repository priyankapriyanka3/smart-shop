/**
 * Utility functions for Smart Shop frontend
 */

/**
 * Class name merger utility (simple implementation without external dependencies)
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}

/**
 * Format currency with locale-aware display
 */
export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

/**
 * Format ISO datetime to readable date and time
 */
export function formatDateTime(isoString: string): string {
  const date = new Date(isoString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

/**
 * Format relative time (e.g., "3 hours ago", "2 days ago")
 */
export function formatRelativeTime(isoString: string): string {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  if (diffSec < 60) return 'just now';
  if (diffMin < 60) return `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
  if (diffHour < 24) return `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`;
  if (diffDay < 30) return `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
  
  return formatDateTime(isoString);
}

/**
 * Get badge color class for order/inventory status
 */
export function getStatusBadgeColor(status: string): string {
  const lowerStatus = status.toLowerCase();
  
  // Success states (green)
  if (['active', 'completed', 'delivered', 'in-stock', 'in_stock', 'approved', 'paid'].includes(lowerStatus)) {
    return 'bg-green-100 text-green-800 border-green-200';
  }
  
  // Warning states (orange)
  if (['pending', 'processing', 'low-stock', 'low_stock', 'shipped', 'under_review'].includes(lowerStatus)) {
    return 'bg-orange-100 text-orange-800 border-orange-200';
  }
  
  // Error states (red)
  if (['failed', 'cancelled', 'out-of-stock', 'out_of_stock', 'rejected', 'inactive'].includes(lowerStatus)) {
    return 'bg-red-100 text-red-800 border-red-200';
  }
  
  // Info states (blue)
  if (['placed', 'new', 'draft'].includes(lowerStatus)) {
    return 'bg-blue-100 text-blue-800 border-blue-200';
  }
  
  // Default (gray)
  return 'bg-gray-100 text-gray-800 border-gray-200';
}

/**
 * Get promotion type badge color
 */
export function getPromotionTypeBadgeColor(type: string): string {
  switch (type.toLowerCase()) {
    case 'percentage':
      return 'bg-purple-100 text-purple-800 border-purple-200';
    case 'fixed':
      return 'bg-indigo-100 text-indigo-800 border-indigo-200';
    case 'free_shipping':
      return 'bg-teal-100 text-teal-800 border-teal-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

/**
 * Truncate text to specified length with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}
