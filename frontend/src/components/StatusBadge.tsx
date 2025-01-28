import { ServiceStatus } from '../types';

interface StatusBadgeProps {
  status: ServiceStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const statusColors = {
    [ServiceStatus.HEALTHY]: 'bg-green-500',
    [ServiceStatus.DEGRADED]: 'bg-yellow-500',
    [ServiceStatus.UNHEALTHY]: 'bg-red-500',
    [ServiceStatus.UNKNOWN]: 'bg-gray-500',
  };

  return (
    <span className={`px-2 py-1 rounded text-white text-sm ${statusColors[status]}`}>
      {status}
    </span>
  );
}
