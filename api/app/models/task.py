from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.category import Category
from app.core.database import Base
from uuid import UUID, uuid4

# --- Tabela asocjacyjna ---
task_applications = Table(
    "task_applications",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("provider_id", ForeignKey("users.id"), primary_key=True)
)


class Task(Base):
    """
    Model zadania łączący klienta i dostawcę.
    """
    __tablename__ = "tasks"

    # Klucz główny
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Pola zadania
    title: Mapped[str] = mapped_column(String, index=True)

    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship()

    details: Mapped[str] = mapped_column(String)

    # Enumy jako Stringi
    budget: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="OPEN")

    distance: Mapped[int] = mapped_column(Integer)
    deadline: Mapped[datetime] = mapped_column(DateTime)

    # Klucze obce
    client_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    provider_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relacje (zdefiniowane jako stringi, by uniknąć importów)
    client = relationship("Client", back_populates="tasks", foreign_keys=[client_id])
    provider = relationship("Provider", back_populates="assigned_tasks", foreign_keys=[provider_id])

    # Lista kandydatów
    # Odwołujemy się do zmiennej task_applications zdefiniowanej wyżej
    candidates = relationship(
        "Provider",
        secondary=task_applications,
        back_populates="applied_tasks"
    )