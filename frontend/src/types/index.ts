import { ServiceStatus } from './health';
import { LogLevel, LogEntry } from './logs';
import { Metric, SystemMetrics } from './metrics';

export { ServiceStatus, LogLevel, LogEntry, Metric, SystemMetrics };

export interface DashboardData {
  services: {
    status: ServiceStatus;
    services: Array<{
      service_id: string;
      service_name: string;
      status: ServiceStatus;
    }>;
  };
  logs: {
    recent: LogEntry[];
    total: number;
  };
  metrics: {
    system: SystemMetrics;
  };
}
