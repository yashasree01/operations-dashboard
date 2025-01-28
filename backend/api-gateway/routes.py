from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .services.health.routes import router as health_router
from .services.logs.routes import router as logs_router
from .services.metrics.routes import router as metrics_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(logs_router)
api_router.include_router(metrics_router)
