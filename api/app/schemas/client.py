from typing import Optional, Literal
from pydantic import BaseModel, EmailStr
from uuid import UUID

from app.schemas.user import UserBase


class ClientBase(UserBase):
    first_name: str
    last_name: str
    phone_number: str
    profile_picture: Optional[str] = None


class CreateClient(ClientBase):
    password: str

    # --- TO POLE JEST KLUCZOWE ---
    role: Literal["CLIENT"] = "CLIENT"


class ClientResponse(ClientBase):
    id: UUID
    is_active: bool = True

    role: Literal["CLIENT"] = "CLIENT"

    class Config:
        from_attributes = True