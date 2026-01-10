from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task


def create_task(
        db: Session,
        client_id: int,
        category: str,
        title: str,
        details: str,
        budget: str,
        distance: int,
        deadline: datetime
) -> Task:
    """
    Funkcja (metoda) tworząca nowe zadanie w bazie danych.
    Przyjmuje czyste argumenty zamiast obiektu schema.
    """
    # Tworzymy instancję modelu bazy danych (SQLAlchemy)
    new_task = Task(
        client_id=client_id,
        category=category,
        title=title,
        details=details,
        budget=budget,
        distance=distance,
        deadline=deadline,
        status="OPEN"  # Wartość domyślna ustawiana w logice
    )

    # Operacje na bazie
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task