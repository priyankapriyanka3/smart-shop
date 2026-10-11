/**
 * Sidebar component for admin and account pages
 */

import { Link, useLocation } from 'react-router-dom';
import { cn } from '../../lib/utils';

interface SidebarItem {
  label: string;
  path: string;
  icon?: React.ReactNode;
}

interface SidebarProps {
  items: SidebarItem[];
  title?: string;
}

export function Sidebar({ items, title }: SidebarProps) {
  const location = useLocation();

  return (
    <aside className="app-sidebar bg-white border-r border-gray-200 min-h-screen p-6">
      {title && (
        <h2 className="text-xl font-bold text-gray-900 mb-6">{title}</h2>
      )}
      
      <nav className="space-y-1">
        {items.map((item) => {
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-blue-600'
              )}
            >
              {item.icon && (
                <span className="mr-3">{item.icon}</span>
              )}
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
