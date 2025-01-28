from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Operations Dashboard API Gateway starting up...")
    yield
    print("Operations Dashboard API Gateway shutting down...")


app = FastAPI(
    title="Operations Dashboard API",
    description="Microservices-based backend for service health, logs, and metrics",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "name": "Operations Dashboard API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
