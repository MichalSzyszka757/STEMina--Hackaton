from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

class Provider(Base):
    """
    Model dostawcy usług (wykonawcy).
    """
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    specialty: Mapped[str] = mapped_column(String, nullable=True)

    # Relacja do zadań
    tasks = relationship("Task", back_populates="provider")

