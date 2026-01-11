from app.core.database import Base
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4

class Category(Base):
    """
    Model kategorii
    """
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)