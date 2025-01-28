import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../services/api';
import { ServiceStatus } from '../types';

interface HealthCheck {
  service_id: string;
  service_name: string;
  status: ServiceStatus;
  response_time_ms: number;
  last_check: string;
}

interface HealthResponse {
  services: HealthCheck[];
  overall_status: ServiceStatus;
  checked_at: string;
}

export function useHealthChecks() {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<HealthResponse>('/health');
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch health checks');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, [fetchHealth]);

  return { data, loading, error, refetch: fetchHealth };
}
