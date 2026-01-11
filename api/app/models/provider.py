from typing import List
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from app.models.user import User, UserRole
from app.models.category import Category, category_provider_association


# USUNIĘTO IMPORT task_applications, aby przerwać pętlę!

class Provider(User):
    """
    Model dostawcy usług (wykonawcy).
    """
    __mapper_args__ = {
        "polymorphic_identity": UserRole.PROVIDER
    }

    # Pola specyficzne dla Providera
    name: Mapped[str] = mapped_column(String, nullable=True)

    # Enums (jako stringi)
    price_tier: Mapped[str] = mapped_column(String, nullable=True)
    lead_time: Mapped[str] = mapped_column(String, nullable=True)

    # Lokalizacja providera
    location: Mapped[int] = mapped_column(Integer, nullable=True)

    starting_year: Mapped[int] = mapped_column(Integer, nullable=True)
    owner: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Kategorie / Specjalizacje
    specialization_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), nullable=True)
    specializations: Mapped[List["Category"]] = relationship("Category", secondary=category_provider_association,
                                                             back_populates="providers")

    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)

    # Relacje do zadań
    assigned_tasks = relationship("Task", back_populates="provider", foreign_keys="Task.provider_id")

    # ZMIANA TUTAJ: Używamy stringa "task_applications" zamiast zmiennej
    applied_tasks = relationship(
        "Task",
        secondary="task_applications",
        back_populates="candidates"
    )