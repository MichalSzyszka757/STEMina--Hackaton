from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importujemy Base z modułu core
from api.app.core.database import Base

class Provider(Base):
    """
    Model dostawcy usług (wykonawcy).
    """
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    specialty: Mapped[str] = mapped_column(String, nullable=True)

    # Relacja do zadań
    tasks = relationship("Task", back_populates="provider")

class Client(Base):
    """
    Model klienta zlecającego.
    """
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="client")

class Task(Base):
    """
    Model zadania łączący klienta i dostawcę.
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Klucze obce
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"))
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("providers.id"))

    # Relacje zwrotne
    client = relationship("Client", back_populates="tasks")
    provider = relationship("Provider", back_populates="tasks")