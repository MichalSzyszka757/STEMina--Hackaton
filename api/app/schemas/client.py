from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.user import UserBase


class ClientCreate(UserBase):
    """
    Schemat używany przy tworzeniu nowego klienta (POST).
    Dziedziczy wszystkie pola z ClientBase.
    """
    first_name: str
    last_name: str
    email: EmailStr  # Automatyczna walidacja formatu email
    phone_number: str
    address: str
    profile_picture: Optional[str] = None

class ClientResponse(UserBase):
    """
    Schemat zwracany przez API (odczyt).
    Zawiera ID nadane przez bazę danych.
    """
    id: int

    class Config:
        # Pozwala Pydanticowi czytać dane bezpośrednio z obiektów SQLAlchemy (ORM)
        from_attributes = True