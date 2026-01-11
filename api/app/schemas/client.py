from typing import Optional, Literal
from pydantic import BaseModel, EmailStr

from app.schemas.user import UserCreate, UserResponse


class ClientCreate(UserCreate):
    """
    Schemat używany przy tworzeniu nowego klienta (POST).
    Dziedziczy wszystkie pola z ClientBase.
    """
    first_name: str
    last_name: str
    phone_number: str
    profile_picture: Optional[str] = None
    role: Literal["CLIENT"]

class ClientResponse(UserResponse):
    """
    Schemat zwracany przez API (odczyt).
    Zawiera ID nadane przez bazę danych.
    """
    id: int

    class Config:
        # Pozwala Pydanticowi czytać dane bezpośrednio z obiektów SQLAlchemy (ORM)
        from_attributes = True