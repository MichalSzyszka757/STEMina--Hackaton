from typing import Optional
from pydantic import BaseModel, EmailStr

class ClientBase(BaseModel):
    """
    Bazowy schemat klienta ze wspólnymi polami.
    """
    first_name: str
    last_name: str
    email: EmailStr  # Automatyczna walidacja formatu email
    phone_number: str
    address: str
    profile_picture: Optional[str] = None

class ClientCreate(ClientBase):
    """
    Schemat używany przy tworzeniu nowego klienta (POST).
    Dziedziczy wszystkie pola z ClientBase.
    """
    pass

class ClientResponse(ClientBase):
    """
    Schemat zwracany przez API (odczyt).
    Zawiera ID nadane przez bazę danych.
    """
    id: int

    class Config:
        # Pozwala Pydanticowi czytać dane bezpośrednio z obiektów SQLAlchemy (ORM)
        from_attributes = True