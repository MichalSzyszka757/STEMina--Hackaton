import sys
import os

# Konfiguracja ścieżki
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.client import Client
from app.models.provider import Provider
from app.models.task import Task
from app.models.category import Category

def check_counts():
    db = SessionLocal()
    try:
        print("--- STATYSTYKI BAZY DANYCH ---")
        print(f"Kategorie: {db.query(Category).count()}")
        print(f"Klienci:   {db.query(Client).count()}")
        print(f"Providerzy:{db.query(Provider).count()}")
        print(f"Zadania:   {db.query(Task).count()}")
        print("------------------------------")
    finally:
        db.close()

if __name__ == "__main__":
    check_counts()