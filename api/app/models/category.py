from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4
from app.core.database import Base

# Tabela asocjacyjna Many-to-Many
category_provider_association = Table(
    "category_provider_association",
    Base.metadata,
    # WAŻNE: Tutaj brakowało ForeignKey!
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    # Provider dziedziczy po User, więc klucz obcy wskazuje na tabelę 'users'
    Column("provider_id", ForeignKey("users.id"), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Relacja do Providera
    # back_populates musi pasować do nazwy pola w modelu Provider ("specializations")
    providers = relationship(
        "Provider",
        secondary=category_provider_association,
        back_populates="specializations"
    )