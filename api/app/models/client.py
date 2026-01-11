from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from app.models.user import UserRole, User


class Client(User):
    """
    Model klienta zlecającego zadania.
    """
    # Dane osobowe/kontaktowe zgodne z ClientBase
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    # Relacja: Klient ma wiele zadań
    # Używamy stringa "Task" aby uniknąć importu pliku task.py tutaj
    tasks = relationship("Task", back_populates="client", cascade="all, delete-orphan", foreign_keys="Task.client_id")

    __mapper_args__ = {
        "polymorphic_identity": UserRole.CLIENT
    }