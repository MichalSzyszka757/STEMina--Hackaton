from typing import List
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
# TERAZ IMPORTUJEMY Z TASK.PY
# Uwaga: Upewnij się, że w task.py nie ma importu "from provider import Provider"
# bo powstanie błędne koło (circular import).
from app.models.task import task_applications
from app.models.user import User, UserRole


class Provider(User):
    """
    Model dostawcy usług (wykonawcy).
    """
    name: Mapped[str] = mapped_column(String, index=True)
    payment: Mapped[int] = mapped_column(Integer)
    deadlines: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String)
    starting_year: Mapped[int] = mapped_column(Integer)
    owner: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    specializations: Mapped[List[str]] = mapped_column(ARRAY(String))

    rating: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

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
