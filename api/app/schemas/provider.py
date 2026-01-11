from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


# --- Klasa Bazowa (Definicja pól) ---
class ProviderBase(BaseModel):
    name: str
    description: str
    starting_year: int
    owner: str

    # --- NOWE POLA DO MATCHINGU ---
    # Enum: "BUDGET", "STANDARD", "PREMIUM"
    price_tier: str

    # Enum: "week", "2week" - jak szybko provider to zrobi
    lead_time: str

    # Lokalizacja providera (do obliczania dystansu do klienta)
    location: int

    # ID kategorii głównej
    specialization_id: UUID


# --- Schemat do tworzenia (Input) ---
class CreateProvider(ProviderBase):
    rating: Optional[float] = 0.0


# --- Schemat do odczytu (Output) ---
class ProviderResponse(ProviderBase):
    id: UUID
    rating: float

    class Config:
        from_attributes = True