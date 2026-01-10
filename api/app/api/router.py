from fastapi import APIRouter
from app.api.endpoints import clients, providers, tasks

api_router = APIRouter()

# Spinamy wszystko w całość:

# Dostępne pod: /api/v1/
api_router.include_router(providers.router, prefix="/providers", tags=["Providers"])

# Dostępne pod: /api/v1/users
api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])

api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])