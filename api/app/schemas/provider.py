from typing import List, Optional, Literal
from pydantic import BaseModel

from app.schemas.user import UserCreate, UserResponse

class ProviderCreate(UserCreate):
    """
    Schemat używany do tworzenia dostawcy (POST).
    Rating i is_active są opcjonalne (mają domyślne wartości).
    """
    rating: Optional[float] = 0.0
    name: str
    payment: int
    deadlines: int  # Np. wskaźnik terminowości
    starting_year: int
    owner: str
    description: str
    specializations: List[str]  # Lista stringów, np. ["Hydraulik", "Elektryk"]

    role: Literal["PROVIDER"]

class ProviderResponse(UserResponse):
    """
    Schemat zwracany przez API (odczyt).
    """
    id: int
    rating: float
    is_active: bool

    class Config:
        from_attributes = True