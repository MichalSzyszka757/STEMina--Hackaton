import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated

# Pobieramy adres bazy danych. Domyślna wartość ustawiona na localhost (dla Podmana/Dockera)
# "postgresql://user:password@localhost:5432/mydatabase"
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/mydatabase"
)

# Tworzymy silnik bazy danych
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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