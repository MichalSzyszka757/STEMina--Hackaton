from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.category import Category
from app.core.database import Base
from uuid import UUID, uuid4

# --- Tabela asocjacyjna (bez zmian) ---
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

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String, index=True)

    # Kategoria zadania (musi pasować do specjalizacji providera)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship()

    details: Mapped[str] = mapped_column(String)

    # ZMIANA NAZEWNICTWA DLA LOGIKI MATCHINGU:

    # 1. Budżet -> PriceTier (Enum jako String: BUDGET/STANDARD/PREMIUM)
    budget: Mapped[str] = mapped_column(String)

    # 2. Status (OPEN/ASSIGNED/COMPLETED)
    status: Mapped[str] = mapped_column(String, default="OPEN")

    # 3. Maksymalny dystans akceptowany przez klienta
    max_distance: Mapped[int] = mapped_column(Integer)

    # 4. NOWOŚĆ: Lokalizacja klienta (do obliczenia różnicy z provider.location)
    client_location: Mapped[int] = mapped_column(Integer, default=0)

    # 5. Deadline (konkretna data - opcjonalnie zostawiamy)
    deadline: Mapped[datetime] = mapped_column(DateTime)

    # 6. NOWOŚĆ: Deadline Limit (Enum: week/2week) - do porównania z provider.lead_time
    deadline_limit: Mapped[str] = mapped_column(String, nullable=True)

    # Klucze obce i relacje (bez większych zmian)
    client_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    provider_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)

    client = relationship("Client", back_populates="tasks", foreign_keys=[client_id])
    provider = relationship("Provider", back_populates="assigned_tasks", foreign_keys=[provider_id])

    candidates = relationship(
        "Provider",
        secondary=task_applications,
        back_populates="applied_tasks"
    )