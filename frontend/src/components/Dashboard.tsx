import { useHealthChecks } from '../services/useHealthChecks';
import { StatusBadge } from './StatusBadge';

export function Dashboard() {
  const { data, loading, error } = useHealthChecks();

  if (loading && !data) {
    return <div className="p-8">Loading...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500">{error}</div>;
  }

  return (
    <div className="dashboard">
      <h1 className="text-2xl font-bold mb-6">Operations Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-sm text-gray-500">Overall Status</h2>
          {data && <StatusBadge status={data.overall_status} />}
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-sm text-gray-500">Services</h2>
          <p className="text-2xl font-bold">{data?.services.length || 0}</p>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-sm text-gray-500">Last Check</h2>
          <p className="text-lg">
            {data?.checked_at ? new Date(data.checked_at).toLocaleTimeString() : 'N/A'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Service Health</h2>
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="pb-2">Service</th>
              <th className="pb-2">Status</th>
              <th className="pb-2">Response Time</th>
            </tr>
          </thead>
          <tbody>
            {data?.services.map((service) => (
              <tr key={service.service_id} className="border-b">
                <td className="py-3">{service.service_name}</td>
                <td className="py-3"><StatusBadge status={service.status} /></td>
                <td className="py-3">{service.response_time_ms.toFixed(0)}ms</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
