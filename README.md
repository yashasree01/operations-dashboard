# Operations Dashboard

Microservices-based backend system to aggregate service health, logs, and operational metrics.

## Structure

```
backend/
├── services/
│   ├── health/        # Service health monitoring
│   ├── logs/         # Log aggregation
│   └── metrics/       # Metrics collection
├── api-gateway/       # API Gateway
└── requirements.txt

frontend/
├── src/
│   ├── components/    # UI components
│   ├── services/      # API integration
│   └── types/         # TypeScript types
└── package.json
```

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn api-gateway.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Services

- **Health Service**: Monitors service status and uptime
- **Logs Service**: Aggregates and indexes logs
- **Metrics Service**: Collects operational metrics
- **API Gateway**: Routes requests to appropriate services
