from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user import User, UserRole


class Client(User):
    """
    Model klienta (zleceniodawcy).
    Dziedziczy ID, email i hasło z modelu User.
    """
    # Konfiguracja dziedziczenia
    __mapper_args__ = {
        "polymorphic_identity": UserRole.CLIENT
    }

    # --- POLA SPECYFICZNE DLA KLIENTA ---
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    # TEGO BRAKOWAŁO (dlatego wywalał błąd):
    address: Mapped[str] = mapped_column(String, nullable=True)

    # To też dodajemy dla pewności (jest w teście):
    phone_number: Mapped[str] = mapped_column(String, nullable=True)

    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    # Relacja do zadań (Tasks)
    tasks = relationship("Task", back_populates="client", foreign_keys="Task.client_id")