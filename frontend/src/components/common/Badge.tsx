/**
 * Reusable Badge component for status indicators
 */

import { cn, getStatusBadgeColor, getPromotionTypeBadgeColor } from '../../lib/utils';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'status' | 'promotion' | 'custom';
  status?: string;
  className?: string;
}

export function Badge({ children, variant = 'status', status, className }: BadgeProps) {
  const baseStyles = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border';
  
  let colorStyles = '';
  
  if (variant === 'status' && status) {
    colorStyles = getStatusBadgeColor(status);
  } else if (variant === 'promotion' && status) {
    colorStyles = getPromotionTypeBadgeColor(status);
  } else if (variant === 'custom') {
    colorStyles = 'bg-gray-100 text-gray-800 border-gray-200';
  }

  return (
    <span className={cn(baseStyles, colorStyles, className)}>
      {children}
    </span>
  );
}
