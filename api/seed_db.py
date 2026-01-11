import sys
import os
import random
from uuid import uuid4
from datetime import datetime, timedelta
from faker import Faker

# --- Konfiguracja środowiska ---
# Dodajemy ścieżkę projektu, aby widzieć folder 'app'
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.client import Client
from app.models.provider import Provider
from app.models.task import Task
from app.models.category import Category
from app.models.enums import PriceTier, LeadTime

# Inicjalizacja Fakera z polskimi danymi
fake = Faker('pl_PL')


def create_random_data():
    """
    Główna funkcja generująca dane testowe.
    Tworzy: Kategorie, Klientów, Providerów i Zadania.
    """
    db = SessionLocal()

    try:
        print("--- [START] Generowanie danych ---")

        # 1. TWORZENIE KATEGORII
        # Lista przykładowych usług
        category_names = ["Fryzjer", "Hydraulik", "Korepetycje", "Mechanik", "Ogród", "Sprzątanie"]
        categories = []

        print(f"-> Tworzenie {len(category_names)} kategorii...")

        # Pętla tworząca kategorie, jeśli jeszcze nie istnieją
        for name in category_names:
            # Sprawdzamy, czy kategoria już jest w bazie (żeby nie dublować)
            existing = db.query(Category).filter_by(name=name).first()
            if not existing:
                cat = Category(id=uuid4(), name=name)
                db.add(cat)
                categories.append(cat)
            else:
                categories.append(existing)

        db.commit()  # Zapisujemy kategorie, by mieć ich ID

        # 2. TWORZENIE KLIENTÓW (10 sztuk)
        clients = []
        print("-> Tworzenie 10 klientów...")

        for _ in range(10):
            # Generowanie losowych danych klienta
            profile = fake.simple_profile()
            client = Client(
                id=uuid4(),
                email_address=profile['mail'],
                hashed_password="hashed_secret_password",  # Hasło "na sztywno" dla testów
                role="CLIENT",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.street_address(),
                city=fake.city(),  # Wymagane pole
                #rating=random.uniform(3.0, 5.0)
            )
            db.add(client)
            clients.append(client)

        db.commit()

        # 3. TWORZENIE PROVIDERÓW (10 sztuk)
        print("-> Tworzenie 10 providerów...")

        # Listy wartości z Enumów do losowania
        tiers = [e.value for e in PriceTier]
        times = [e.value for e in LeadTime]

        for _ in range(10):
            # Losujemy kategorię dla providera
            random_cat = random.choice(categories)
            profile = fake.simple_profile()

            provider = Provider(
                id=uuid4(),
                email_address=fake.email(),  # Unikalny email
                hashed_password="hashed_secret_password",
                role="PROVIDER",
                name=f"Firma {fake.company()}",
                description=fake.catch_phrase(),
                city="Kraków",  # Ustawiamy Kraków, żeby łatwiej o Match
                #address=fake.street_address(),
                #phone_number=fake.phone_number(),

                # Pola specyficzne dla matchingu
                specialization_id=random_cat.id,
                price_tier=random.choice(tiers),
                lead_time=random.choice(times),
                location=random.randint(0, 30),  # Dystans 0-30 km od centrum
                rating=random.uniform(2.0, 5.0),
                starting_year=random.randint(2010, 2023),
                owner=fake.name()
            )
            db.add(provider)

        db.commit()

        # 4. TWORZENIE ZADAŃ (20 sztuk)
        print("-> Tworzenie 20 zadań...")

        for _ in range(20):
            # Losujemy klienta i kategorię
            random_client = random.choice(clients)
            random_cat = random.choice(categories)

            task = Task(
                client_id=random_client.id,
                category_id=random_cat.id,
                title=f"Szukam: {random_cat.name}",
                details=fake.text(max_nb_chars=100),

                # Pola matchingu (wymagania klienta)
                budget=random.choice(tiers),
                deadline_limit=random.choice(times),
                client_location=0,  # Klient jest w centrum (0)
                max_distance=random.randint(10, 50),  # Szuka w promieniu 10-50km

                status="OPEN",
                deadline=datetime.now() + timedelta(days=random.randint(5, 30))
            )
            db.add(task)

        db.commit()
        print("--- [SUKCES] Baza została wypełniona! ---")

    except Exception as e:
        # Wypisanie błędu, jeśli coś pójdzie nie tak
        print(f"--- [BŁĄD] {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_random_data()