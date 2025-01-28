from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry(BaseModel):
    id: str
    timestamp: datetime
    level: LogLevel
    service: str
    message: str
    metadata: Optional[Dict] = None


class LogQuery(BaseModel):
    service: Optional[str] = None
    level: Optional[LogLevel] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    search: Optional[str] = None
    limit: int = 100
    offset: int = 0


class LogResponse(BaseModel):
    logs: List[LogEntry]
    total: int
    query: LogQuery
