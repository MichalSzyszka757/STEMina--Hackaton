from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserType(str, Enum):
    client = "CLIENT"
    provider = "PROVIDER"

class UserBase(BaseModel):
    email_address: Optional[str] = EmailStr
    #disabled: Optional[bool] = None
    account_type: UserType
    city: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    pass

class User(UserBase):
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
