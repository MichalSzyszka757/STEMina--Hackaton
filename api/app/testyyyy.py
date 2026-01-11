import sys
import os
from uuid import uuid4
from datetime import datetime

# Dodajemy katalog bieżący do ścieżki, aby Python widział moduły 'app'
sys.path.append(os.getcwd())

from core.database import SessionLocal, Base, engine
from models.task import Task
from models.provider import Provider
from models.client import Client  # Zakładam, że masz ten model
from models.category import Category  # Potrzebne do relacji
from models.enums import PriceTier, LeadTime
from services.matching_service import find_matches_for_task


def run_matching_test():
    """
    Skrypt testujący logikę dopasowywania (Matching Service).
    Symuluje Tindera dla usług: Task vs Providers.
    """
    print("--- [START] RESETOWANIE BAZY DANYCH ---")
    # 1. Usuwamy stare tabele i tworzymy nowe (żeby mieć pewność co do struktury)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("--- [KROK 1] TWORZENIE DANYCH ---")

        # Tworzymy kategorię (np. Fryzjer)
        cat_hair = Category(id=uuid4(), name="Fryzjer")
        db.add(cat_hair)
        db.commit()

        # Tworzymy Klienta (Jana)
        client_jan = Client(
            id=uuid4(),
            first_name="Jan",
            last_name="Klient",
            email="jan@test.pl",
            phone_number="123",
            address="Krk",
            hashed_password="xxx",  # Wymagane przez model User
            role="CLIENT"
        )
        db.add(client_jan)
        db.commit()

        # --- TWORZENIE ZADANIA (OCZEKIWANIA) ---
        # Jan szuka fryzjera:
        # - Cena: STANDARD
        # - Czas: Ma być zrobione w max 2 tygodnie ("2week")
        # - Lokalizacja: Jan jest w punkcie 0, szuka kogoś w promieniu 20 km
        task = Task(
            client_id=client_jan.id,
            category_id=cat_hair.id,
            title="Strzyżenie męskie",
            details="Krótko",
            budget=PriceTier.STANDARD,  # Oczekiwanie cenowe
            deadline_limit=LeadTime.TWO_WEEKS,  # Oczekiwanie czasowe
            client_location=0,  # Gdzie jest klient
            max_distance=20,  # Jak daleko może podjechać (lub provider do niego)
            status="OPEN",
            deadline=datetime.now()
        )
        db.add(task)
        db.commit()
        print(f"ZADANIE UTWORZONE: {task.title} | Budżet: {task.budget} | Max Dystans: {task.max_distance}")

        # --- TWORZENIE KANDYDATÓW (OFERTY) ---

        # 1. Provider IDEALNY (Pasuje wszystko)
        p_match = Provider(
            id=uuid4(), email="match@p.pl", hashed_password="x", role="PROVIDER",  # Pola Usera
            name="Salon Idealny",
            specialization_id=cat_hair.id,  # Ta sama kategoria
            price_tier=PriceTier.STANDARD,  # Ta sama cena
            lead_time=LeadTime.ONE_WEEK,  # Robi w 1 tydzień (mieści się w limicie 2 tyg) -> OK
            location=10  # Odległość 10km (mieści się w 20km) -> OK
        )

        # 2. Provider ZA DROGI (Mismatch: Price)
        p_expensive = Provider(
            id=uuid4(), email="drogi@p.pl", hashed_password="x", role="PROVIDER",
            name="Salon Ekskluzywny",
            specialization_id=cat_hair.id,
            price_tier=PriceTier.PREMIUM,  # PREMIUM vs STANDARD -> ODRZUT (SQL)
            lead_time=LeadTime.ONE_WEEK,
            location=10
        )

        # 3. Provider ZA WOLNY (Mismatch: Time)
        p_slow = Provider(
            id=uuid4(), email="wolny@p.pl", hashed_password="x", role="PROVIDER",
            name="Salon Powolny",
            specialization_id=cat_hair.id,
            price_tier=PriceTier.STANDARD,
            lead_time=LeadTime.THREE_WEEKS,  # 3 tygodnie vs Limit 2 tygodnie -> ODRZUT (Python)
            location=10
        )

        # 4. Provider ZA DALEKO (Mismatch: Distance)
        p_far = Provider(
            id=uuid4(), email="daleko@p.pl", hashed_password="x", role="PROVIDER",
            name="Salon Daleki",
            specialization_id=cat_hair.id,
            price_tier=PriceTier.STANDARD,
            lead_time=LeadTime.ONE_WEEK,
            location=50  # 50km vs Limit 20km -> ODRZUT (Python)
        )

        db.add_all([p_match, p_expensive, p_slow, p_far])
        db.commit()
        print("KANDYDACI DODANI: Idealny, Za Drogi, Za Wolny, Za Daleki")

        print("\n--- [KROK 2] URUCHOMIENIE MATCHINGU ---")

        # Wywołujemy naszą funkcję logiczną
        matches = find_matches_for_task(db, task.id)

        print(f"Liczba pasujących ofert: {len(matches)}")

        # --- WERYFIKACJA WYNIKÓW ---
        found_names = [p.name for p in matches]
        print(f"Znaleziono: {found_names}")

        if "Salon Idealny" in found_names and len(matches) == 1:
            print("\n[SUKCES] Algorytm działa poprawnie! Znalazł tylko pasującego providera.")
        else:
            print("\n[BŁĄD] Algorytm zwrócił złe wyniki.")

    except Exception as e:
        print(f"[WYJĄTEK] Coś poszło nie tak: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_matching_test()