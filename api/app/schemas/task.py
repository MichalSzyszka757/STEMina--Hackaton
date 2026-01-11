from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# --- Klasa Bazowa (Definicja pól) ---
class TaskBase(BaseModel):
    title: str
    details: str

    # ID kategorii (np. UUID fryzjera)
    category_id: UUID

    # --- NOWE POLA DO MATCHINGU ---
    # Enum: "BUDGET", "STANDARD", "PREMIUM"
    budget: str

    # Maksymalna odległość od providera (w km)
    max_distance: int

    # Lokalizacja klienta (np. kod pocztowy lub int) - potrzebna do obliczenia dystansu
    client_location: int

    # Enum: "week", "2week" - ile czasu ma provider
    deadline_limit: str


# --- Schemat do tworzenia (Input) ---
class CreateTask(TaskBase):
    # Te pola są wymagane przy tworzeniu
    pass


# --- Schemat do odczytu (Output) ---
class TaskResponse(TaskBase):
    id: UUID
    status: str  # np. "OPEN"
    client_id: UUID
    provider_id: Optional[UUID] = None

    class Config:
        from_attributes = True