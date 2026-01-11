from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserType(str, Enum):
    client = "CLIENT"
    provider = "PROVIDER"

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    account_type: UserType

class UserCreate(UserBase):
    password: str

class User(UserBase):
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
