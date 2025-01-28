from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import random
import uuid

from .models import LogEntry, LogResponse, LogQuery, LogLevel


router = APIRouter(prefix="/logs", tags=["logs"])

MOCK_SERVICES = ["api-gateway", "auth-service", "user-service", "payment-service"]

LOG_MESSAGES = {
    LogLevel.DEBUG: [
        "Processing request details",
        "Cache miss for key: user_preferences",
        "Query executed in 5ms",
    ],
    LogLevel.INFO: [
        "Request processed successfully",
        "User authenticated",
        "New connection established",
    ],
    LogLevel.WARNING: [
        "High memory usage detected: 85%",
        "Slow query detected: 500ms",
        "Rate limit approaching: 80%",
    ],
    LogLevel.ERROR: [
        "Failed to connect to database",
        "Authentication failed for user",
        "Request timeout after 30s",
    ],
    LogLevel.CRITICAL: [
        "System out of memory",
        "Database connection lost",
        "Service unavailable",
    ],
}


def generate_mock_logs(count: int = 50) -> List[LogEntry]:
    logs = []
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    for i in range(count):
        level_weights = [10, 50, 25, 12, 3]
        levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]
        level = random.choices(levels, weights=level_weights)[0]
        
        logs.append(LogEntry(
            id=str(uuid.uuid4()),
            timestamp=base_time + timedelta(minutes=i * 30),
            level=level,
            service=random.choice(MOCK_SERVICES),
            message=random.choice(LOG_MESSAGES[level]),
            metadata={"request_id": str(uuid.uuid4())[:8]}
        ))
    
    return logs


@router.get("", response_model=LogResponse)
async def get_logs(
    service: Optional[str] = Query(None),
    level: Optional[LogLevel] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    logs = generate_mock_logs(count=200)
    
    if service:
        logs = [log for log in logs if log.service == service]
    if level:
        logs = [log for log in logs if log.level == level]
    if start_time:
        logs = [log for log in logs if log.timestamp >= start_time]
    if end_time:
        logs = [log for log in logs if log.timestamp <= end_time]
    if search:
        logs = [log for log in logs if search.lower() in log.message.lower()]
    
    logs.sort(key=lambda x: x.timestamp, reverse=True)
    
    total = len(logs)
    paginated_logs = logs[offset:offset + limit]
    
    return LogResponse(
        logs=paginated_logs,
        total=total,
        query=LogQuery(
            service=service,
            level=level,
            start_time=start_time,
            end_time=end_time,
            search=search,
            limit=limit,
            offset=offset
        )
    )


@router.get("/services", response_model=List[str])
async def get_log_services():
    return MOCK_SERVICES


@router.get("/stats")
async def get_log_stats():
    logs = generate_mock_logs(count=500)
    
    by_service = defaultdict(int)
    by_level = defaultdict(int)
    
    for log in logs:
        by_service[log.service] += 1
        by_level[log.level] += 1
    
    return {
        "total_logs": len(logs),
        "by_service": dict(by_service),
        "by_level": {k: v for k, v in by_level.items()},
        "time_range": {
            "oldest": min(log.timestamp for log in logs),
            "newest": max(log.timestamp for log in logs)
        }
    }
