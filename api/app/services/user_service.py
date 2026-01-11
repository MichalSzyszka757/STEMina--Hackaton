from typing import Literal, Union, Annotated
from pydantic import Field
from sqlalchemy import select

from app.core.database import SessionDep
from app.core import security

from app.schemas.user import UserInDB, UserType
from app.schemas.client import ClientCreate
from app.schemas.provider import ProviderCreate

from app.models import Client, User, Provider


# Nasza udawana baza
# Hasło: tajnehaslo123
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$/P6XgLgNNxa6oVL8NuUPhg$YeOm7vdhbHOSht0NzlBqWvdLUZpv0cYZxQJ6ik34XEI",
        "disabled": False,
    }
}

def get_user_by_username(session: SessionDep, email_address: str) -> UserInDB | None:
    statement = select(User).where(User.email_address == email_address)

    return session.execute(statement).scalar_one_or_none()


UserRegister = Annotated[Union[ClientCreate, ProviderCreate], Field(discriminator="role")]

def create_user(session: SessionDep, user_data: UserRegister) -> UserInDB | None:
    
    obj_data = user_data.model_dump(exclude={'password', 'account_type'})

    if isinstance(user_data, ClientCreate):
        db_obj = Client(**obj_data, hashed_password=security.get_password_hash(user_data.password))
    elif isinstance(user_data, ProviderCreate):
        db_obj = Provider(**obj_data, hashed_password=security.get_password_hash(user_data.password))

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj