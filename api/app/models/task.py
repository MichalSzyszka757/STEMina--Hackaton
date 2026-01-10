from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

# --- Tabela asocjacyjna ---
task_applications = Table(
    "task_applications",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("provider_id", Integer, ForeignKey("providers.id"), primary_key=True)
)


class Task(Base):
    """
    Model zadania łączący klienta i dostawcę.
    """
    __tablename__ = "tasks"

    # Klucz główny
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Pola zadania
    category: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    details: Mapped[str] = mapped_column(String)

    # Enumy jako Stringi
    budget: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="OPEN")

    distance: Mapped[int] = mapped_column(Integer)
    deadline: Mapped[datetime] = mapped_column(DateTime)

    # Klucze obce
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"))
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("providers.id"), nullable=True)

    # Relacje (zdefiniowane jako stringi, by uniknąć importów)
    client = relationship("Client", back_populates="tasks")
    provider = relationship("Provider", back_populates="assigned_tasks")

    # Lista kandydatów
    # Odwołujemy się do zmiennej task_applications zdefiniowanej wyżej
    candidates = relationship(
        "Provider",
        secondary=task_applications,
        back_populates="applied_tasks"
    )