/**
 * Route guard component that redirects to login if not authenticated
 */

import { Navigate } from 'react-router-dom';
import { useAuth } from '../../lib/auth-context';
import sharedConfig from '../../../../shared_config.json';

interface RequireAuthProps {
  children: React.ReactNode;
  requiredRole?: string;
}

export function RequireAuth({ children, requiredRole }: RequireAuthProps) {
  const { isAuthenticated, isLoading, user } = useAuth();
  
  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
          <p className="mt-2 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }
  
  // Check if token exists in localStorage
  const token = localStorage.getItem(sharedConfig.auth.storage_key);
  
  // Redirect to login if not authenticated
  if (!isAuthenticated && !token) {
    return <Navigate to="/login" replace />;
  }
  
  // Check role if required
  if (requiredRole && user && user.role !== requiredRole) {
    // User is authenticated but doesn't have required role
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-2">Access Denied</h1>
          <p className="text-gray-600">You do not have permission to access this page.</p>
        </div>
      </div>
    );
  }
  
  return <>{children}</>;
}
