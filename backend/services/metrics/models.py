from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


class MetricPoint(BaseModel):
    timestamp: datetime
    value: float


class Metric(BaseModel):
    name: str
    type: MetricType
    unit: str
    description: str
    current_value: float
    history: List[MetricPoint]


class MetricsResponse(BaseModel):
    metrics: List[Metric]
    collected_at: datetime


class SystemMetrics(BaseModel):
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_in_mbps: float
    network_out_mbps: float
    active_connections: int
    requests_per_second: float
    error_rate_percent: float
