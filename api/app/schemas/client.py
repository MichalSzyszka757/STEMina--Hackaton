from typing import Optional, Literal
from pydantic import BaseModel, EmailStr
from uuid import UUID


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
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