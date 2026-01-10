
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

class Client(Base):
    """
    Model klienta zlecającego.
    """
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="client")