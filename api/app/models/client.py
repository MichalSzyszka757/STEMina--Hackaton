from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class Client(Base):
    """
    Model klienta zlecającego zadania.
    """
    __tablename__ = "clients"

    # Klucz główny jako Integer
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Dane osobowe/kontaktowe zgodne z ClientBase
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    # Relacja: Klient ma wiele zadań
    # Używamy stringa "Task" aby uniknąć importu pliku task.py tutaj
    tasks = relationship("Task", back_populates="client", cascade="all, delete-orphan")