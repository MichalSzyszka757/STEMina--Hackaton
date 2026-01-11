from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID

from app.core.database import Base

class UserRole(str, Enum):
    CLIENT = "CLIENT"
    PROVIDER = "PROVIDER"
    ADMIN = "ADMIN"

# --- MODEL GŁÓWNY (USER) ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email_address: Mapped[str] = mapped_column(String(255),  unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # To pole decyduje, czy wiersz jest Clientem czy Providerem
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False)

    # Konfiguracja Polimorfizmu
    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": "USER"
    }