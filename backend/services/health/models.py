from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheck(BaseModel):
    service_id: str
    service_name: str
    status: ServiceStatus
    response_time_ms: float
    last_check: datetime
    details: Optional[Dict] = None


class ServiceHealthResponse(BaseModel):
    services: List[HealthCheck]
    overall_status: ServiceStatus
    checked_at: datetime


class HealthCheckRequest(BaseModel):
    service_ids: Optional[List[str]] = None
    include_details: bool = True
