from fastapi import APIRouter
from app.schemas.client import CreateClient
from app.schemas.provider import CreateProvider
from app.schemas.user import UserType, UserInDB
from app.core.database import SessionDep
from app.services import user_service
from app.services.user_service import UserRegister

from app.schemas.client import CreateClient    # <--- Zmiana nazwy
from app.schemas.provider import CreateProvider # <--- Zmiana nazwy
router = APIRouter()

db_session = None

@router.get("/")
def get_users_specific_type(type: UserType):
    pass

@router.post("/", status_code=201)
def register_user(session: SessionDep, user_data: UserRegister) -> UserInDB:
    return user_service.create_user(session, user_data)