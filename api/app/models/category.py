from typing import List
from app.core.database import Base
from sqlalchemy import Boolean, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4

# --- Tabela asocjacyjna ---
category_provider_association = Table(
    "category_provider_association",
    Base.metadata,
    Column("category_id", ForeignKey("tasks.id"), primary_key=True),
    Column("provider_id", ForeignKey("users.id"), primary_key=True)
)


class Category(Base):
    """
    Model kategorii
    """
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)

    providers: Mapped[List["Provider"]] = relationship("Provider", secondary=category_provider_association, back_populates="providers")