from typing import List, Optional, Literal
from pydantic import BaseModel
from uuid import UUID
from app.models.enums import PriceTier, LeadTime
from app.schemas.user import UserBase


class ProviderBase(UserBase):
    """
    Pola wspólne dla dostawcy.
    """
    name: str
    description: str
    owner: str
    starting_year: int

    # POLA DO MATCHINGU
    price_tier: PriceTier
    lead_time: LeadTime

    specialization_id: UUID


class CreateProvider(ProviderBase):
    """
    Model wejściowy (Input) - Rejestracja dostawcy.
    """
    password: str
    rating: Optional[float] = 0.0

    # --- TO POLE JEST KLUCZOWE DLA NAPRAWY BŁĘDU ---
    role: Literal["PROVIDER"] = "PROVIDER"


class ProviderResponse(ProviderBase):
    """
    Model wyjściowy (Output).
    """
    id: UUID
    rating: float
    is_active: bool = True

    role: Literal["PROVIDER"] = "PROVIDER"

    class Config:
        from_attributes = True