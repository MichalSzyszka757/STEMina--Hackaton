import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated

# --- ZMIANA NA SQLITE ---
# Zamiast łączyć się z Dockerem, tworzymy plik bazy danych w folderze api
SQLALCHEMY_DATABASE_URL = "sqlite:///./baza_hackaton.db"

# Tworzymy silnik bazy danych
# connect_args={"check_same_thread": False} jest wymagane tylko dla SQLite w FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Fabryka sesji - tworzy nowe połączenia dla każdego żądania
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla modeli ORM
Base = declarative_base()

# Funkcja zależna (dependency) do wstrzykiwania sesji DB
def get_db():
    """
    Tworzy sesję bazy danych dla żądania i zamyka ją po zakończeniu.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Zawsze zamykaj sesję, nawet w przypadku błędu
        db.close()

SessionDep = Annotated[SessionLocal, Depends(get_db)]