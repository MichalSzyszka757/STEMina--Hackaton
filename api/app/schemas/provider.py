from typing import List, Optional
from pydantic import BaseModel

from app.schemas.user import UserBase

class ProviderCreate(UserBase):
    """
    Schemat używany do tworzenia dostawcy (POST).
    Rating i is_active są opcjonalne (mają domyślne wartości).
    """
    rating: Optional[float] = 0.0
    is_active: Optional[bool] = True
    name: str
    payment: int
    deadlines: int  # Np. wskaźnik terminowości
    location: str   # Odpowiednik pola distance z modelu (lokalizacja)
    starting_year: int
    owner: str
    description: str
    specializations: List[str]  # Lista stringów, np. ["Hydraulik", "Elektryk"]

class ProviderResponse(UserBase):
    """
    Schemat zwracany przez API (odczyt).
    """
    id: int
    rating: float
    is_active: bool

    class Config:
        from_attributes = True