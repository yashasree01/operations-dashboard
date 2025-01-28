from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import random

from .models import Metric, MetricPoint, MetricsResponse, SystemMetrics, MetricType


router = APIRouter(prefix="/metrics", tags=["metrics"])

METRIC_DEFINITIONS = [
    {"name": "cpu_usage", "type": MetricType.GAUGE, "unit": "percent", "description": "CPU utilization"},
    {"name": "memory_usage", "type": MetricType.GAUGE, "unit": "percent", "description": "Memory utilization"},
    {"name": "disk_usage", "type": MetricType.GAUGE, "unit": "percent", "description": "Disk utilization"},
    {"name": "request_count", "type": MetricType.COUNTER, "unit": "count", "description": "Total requests"},
    {"name": "response_time_p50", "type": MetricType.HISTOGRAM, "unit": "ms", "description": "P50 response time"},
    {"name": "response_time_p95", "type": MetricType.HISTOGRAM, "unit": "ms", "description": "P95 response time"},
    {"name": "error_rate", "type": MetricType.GAUGE, "unit": "percent", "description": "Error rate"},
    {"name": "active_connections", "type": MetricType.GAUGE, "unit": "count", "description": "Active connections"},
]


def generate_metric_history(name: str, base_value: float, variance: float) -> List[MetricPoint]:
    history = []
    current_value = base_value
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    for i in range(288):
        current_value = max(0, min(100, current_value + random.uniform(-variance, variance)))
        history.append(MetricPoint(
            timestamp=base_time + timedelta(minutes=i * 5),
            value=round(current_value, 2)
        ))
    
    return history


def get_metric_current_value(name: str) -> float:
    if name in ["cpu_usage", "memory_usage", "disk_usage"]:
        return round(random.uniform(30, 80), 2)
    elif name == "request_count":
        return random.randint(10000, 100000)
    elif name in ["response_time_p50", "response_time_p95"]:
        return round(random.uniform(50, 500), 2)
    elif name == "error_rate":
        return round(random.uniform(0, 5), 2)
    else:
        return round(random.uniform(0, 100), 2)


@router.get("", response_model=MetricsResponse)
async def get_all_metrics():
    metrics = []
    
    for defn in METRIC_DEFINITIONS:
        base_value = get_metric_current_value(defn["name"])
        variance = 10 if defn["type"] == MetricType.GAUGE else 50
        
        metrics.append(Metric(
            name=defn["name"],
            type=defn["type"],
            unit=defn["unit"],
            description=defn["description"],
            current_value=base_value,
            history=generate_metric_history(defn["name"], base_value, variance)
        ))
    
    return MetricsResponse(
        metrics=metrics,
        collected_at=datetime.utcnow()
    )


@router.get("/system", response_model=SystemMetrics)
async def get_system_metrics():
    return SystemMetrics(
        cpu_usage_percent=round(random.uniform(20, 85), 2),
        memory_usage_percent=round(random.uniform(40, 90), 2),
        disk_usage_percent=round(random.uniform(30, 70), 2),
        network_in_mbps=round(random.uniform(10, 100), 2),
        network_out_mbps=round(random.uniform(5, 50), 2),
        active_connections=random.randint(10, 500),
        requests_per_second=round(random.uniform(100, 1000), 2),
        error_rate_percent=round(random.uniform(0, 3), 2)
    )


@router.get("/{metric_name}", response_model=Metric)
async def get_metric(metric_name: str):
    metric_def = next(
        (m for m in METRIC_DEFINITIONS if m["name"] == metric_name),
        None
    )
    
    if not metric_def:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    current_value = get_metric_current_value(metric_name)
    variance = 10 if metric_def["type"] == MetricType.GAUGE else 50
    
    return Metric(
        name=metric_def["name"],
        type=metric_def["type"],
        unit=metric_def["unit"],
        description=metric_def["description"],
        current_value=current_value,
        history=generate_metric_history(metric_name, current_value, variance)
    )
