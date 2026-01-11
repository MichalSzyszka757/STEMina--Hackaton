from fastapi import APIRouter
from app.schemas.client import ClientCreate
from app.schemas.provider import ProviderCreate
from app.schemas.user import UserType

from app.services import user_service
from app.services.user_service import UserRegister

router = APIRouter()

@router.get("/")
def get_users_specific_type(type: UserType):
    pass

@router.post("/", status_code=201)
def register_user(user_data: UserRegister) -> UserRegister:
    return user_service.create_user(user_data)