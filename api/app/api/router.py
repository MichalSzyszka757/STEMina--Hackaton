from fastapi import APIRouter
from app.api.endpoints import tasks, auth, users

api_router = APIRouter()

# Spinamy wszystko w całość:

# Dostępne pod: /api/v1/
# api_router.include_router(providers.router, prefix="/providers", tags=["Providers"])

# Dostępne pod: /api/v1/users
# api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])

api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

api_router.include_router(users.router, prefix="/users", tags=["Users"])

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])