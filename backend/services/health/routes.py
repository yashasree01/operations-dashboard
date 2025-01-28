from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
import random

from .models import (
    ServiceStatus,
    HealthCheck,
    ServiceHealthResponse,
    HealthCheckRequest
)


router = APIRouter(prefix="/health", tags=["health"])

MOCK_SERVICES = [
    {"id": "api-gateway", "name": "API Gateway"},
    {"id": "auth-service", "name": "Authentication Service"},
    {"id": "user-service", "name": "User Service"},
    {"id": "payment-service", "name": "Payment Service"},
    {"id": "notification-service", "name": "Notification Service"},
    {"id": "analytics-service", "name": "Analytics Service"},
]


async def perform_health_check(service_id: str, service_name: str) -> HealthCheck:
    await asyncio.sleep(0.01)
    
    response_time = random.uniform(10, 150)
    statuses = [ServiceStatus.HEALTHY, ServiceStatus.HEALTHY, ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]
    status = random.choice(statuses)
    
    return HealthCheck(
        service_id=service_id,
        service_name=service_name,
        status=status,
        response_time_ms=response_time,
        last_check=datetime.utcnow(),
        details={"uptime_seconds": random.randint(86400, 2592000)}
    )


@router.get("", response_model=ServiceHealthResponse)
async def get_all_health_checks():
    tasks = [
        perform_health_check(svc["id"], svc["name"])
        for svc in MOCK_SERVICES
    ]
    results = await asyncio.gather(*tasks)
    services = list(results)
    
    unhealthy_count = sum(
        1 for s in services 
        if s.status in (ServiceStatus.UNHEALTHY, ServiceStatus.UNKNOWN)
    )
    degraded_count = sum(
        1 for s in services 
        if s.status == ServiceStatus.DEGRADED
    )
    
    if unhealthy_count > 0:
        overall = ServiceStatus.UNHEALTHY
    elif degraded_count > 0:
        overall = ServiceStatus.DEGRADED
    else:
        overall = ServiceStatus.HEALTHY
    
    return ServiceHealthResponse(
        services=services,
        overall_status=overall,
        checked_at=datetime.utcnow()
    )


@router.post("/check", response_model=ServiceHealthResponse)
async def check_services(request: HealthCheckRequest):
    services_to_check = MOCK_SERVICES
    
    if request.service_ids:
        services_to_check = [
            svc for svc in MOCK_SERVICES 
            if svc["id"] in request.service_ids
        ]
    
    tasks = [
        perform_health_check(svc["id"], svc["name"])
        for svc in services_to_check
    ]
    results = await asyncio.gather(*tasks)
    
    return ServiceHealthResponse(
        services=list(results),
        overall_status=ServiceStatus.HEALTHY,
        checked_at=datetime.utcnow()
    )


@router.get("/{service_id}", response_model=HealthCheck)
async def get_service_health(service_id: str):
    service = next(
        (svc for svc in MOCK_SERVICES if svc["id"] == service_id),
        None
    )
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return await perform_health_check(service["id"], service["name"])
