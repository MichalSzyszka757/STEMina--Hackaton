from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Bazowy schemat zadania z polami wspólnymi
class TaskBase(BaseModel):
    category: str
    title: str
    details: str
    budget: str      # Typ budżetu, np. "STANDARD" lub "BUDGET"
    distance: int    # Wymagany dystans/lokalizacja
    deadline: datetime

# Schemat służący do tworzenia nowego zadania (mutowalny)
class CreateTask(TaskBase):
    # Musimy wiedzieć, który klient tworzy zadanie
    client_id: int
    # Status domyślnie ustawia się na "OPEN" w bazie, więc tu jest pominięty

# Schemat zwracany przez API (odczyt)
class TaskResponse(TaskBase):
    id: int
    status: str      # Np. "OPEN", "ASSIGNED", "COMPLETED"
    client_id: int
    # Może być null (None), jeśli wykonawca nie został jeszcze wybrany
    provider_id: Optional[int] = None

    class Config:
        # Umożliwia mapowanie z obiektu SQLAlchemy
        from_attributes = True