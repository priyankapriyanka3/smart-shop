type StatusType = 'delivered' | 'shipped' | 'confirmed' | 'pending' | 'processing';

interface StatusBadgeProps {
  status: StatusType | string;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const getStatusStyles = (status: string) => {
    switch (status.toLowerCase()) {
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'shipped':
        return 'bg-blue-100 text-blue-900';
      case 'confirmed':
        return 'bg-blue-100 text-blue-900';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
  };

  return (
    <span
      className={`inline-block px-3 py-1.5 rounded-xl text-xs font-semibold ${getStatusStyles(
        status
      )}`}
    >
      {getStatusLabel(status)}
    </span>
  );
}
