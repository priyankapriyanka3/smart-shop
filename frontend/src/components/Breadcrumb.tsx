import { Link } from 'react-router-dom';

export interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav className="bg-white py-4 px-8 border-b border-gray-200">
      <div className="max-w-[1400px] mx-auto flex gap-2 items-center text-sm">
        {items.map((item, index) => (
          <span key={index} className="flex items-center gap-2">
            {item.path ? (
              <Link to={item.path} className="text-blue-600 no-underline hover:underline">
                {item.label}
              </Link>
            ) : (
              <span className="text-gray-700 font-medium">{item.label}</span>
            )}
            {index < items.length - 1 && <span className="text-gray-600">›</span>}
          </span>
        ))}
      </div>
    </nav>
  );
}
