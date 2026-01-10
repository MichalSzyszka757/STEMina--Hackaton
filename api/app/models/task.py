
class Task(Base):
    """
    Model zadania łączący klienta i dostawcę.
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Klucze obce
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"))
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("providers.id"))

    # Relacje zwrotne
    client = relationship("Client", back_populates="tasks")
    provider = relationship("Provider", back_populates="tasks")