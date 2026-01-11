from typing import List
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from app.core.database import Base
# TERAZ IMPORTUJEMY Z TASK.PY
# Uwaga: Upewnij się, że w task.py nie ma importu "from provider import Provider"
# bo powstanie błędne koło (circular import).
from app.models.task import task_applications
from app.models.user import User, UserRole

from app.models.category import category_provider_association


class Provider(User):
    """
    Model dostawcy usług (wykonawcy).
    """
    name: Mapped[str] = mapped_column(String, nullable=True)
    payment: Mapped[int] = mapped_column(Integer, nullable=True)
    deadlines: Mapped[int] = mapped_column(Integer, nullable=True)
    starting_year: Mapped[int] = mapped_column(Integer, nullable=True)
    owner: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    
    specialization_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    specializations: Mapped[List["Category"]] = relationship("Category", secondary=category_provider_association, back_populates="categories")

    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)

    assigned_tasks = relationship("Task", back_populates="provider", foreign_keys="Task.provider_id")

    # Relacja kandydatów używa teraz importu z task.py
    applied_tasks = relationship(
        "Task",
        secondary=task_applications,
        back_populates="candidates"
    )

    __mapper_args__ = {
        "polymorphic_identity": UserRole.PROVIDER
    }
