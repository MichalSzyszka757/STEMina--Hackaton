import csv
import random
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from faker import Faker

from sqlalchemy.orm import Session
# Import konfiguracji bazy i modeli
from api.app.core.database import engine, get_db
from api.app.models import models

# Tworzenie tabel w bazie danych, jeśli nie istnieją
# SQLAlchemy skanuje modele zaimportowane w 'models' i tworzy strukturę
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint testowy. Sprawdza połączenie z bazą.
    """
    # Jeśli dependency zadziałało, baza jest połączona
    return {"status": "ok", "db": "connected"}


# Inicjalizacja polskiej lokalizacji
fake = Faker('pl_PL')

# Lista przykładowych ulic w Krakowie dla zwiększenia realizmu
KRAKOW_STREETS = [
    "Floriańska", "Grodzka", "Szewska", "Karmelicka", "Miodowa",
    "Starowiślna", "Kazimierza Wielkiego", "Mogilska", "Dietla",
    "Grzegórzecka", "Kalwaryjska", "Kościuszki", "Czarnowiejska",
    "Pawia", "Lubicz", "Rakowicka", "Balicka", "Wielicka"
]


def generuj_krakowski_adres():
    ulica = random.choice(KRAKOW_STREETS)
    nr_domu = fake.building_number()
    # Losujemy kod pocztowy z zakresu krakowskiego (30-xxx do 31-xxx)
    kod_pocztowy = f"{random.randint(30, 31)}-{random.randint(100, 999)}"
    return f"ul. {ulica} {nr_domu}, {kod_pocztowy} Kraków"


def generuj_i_zapisz_do_csv(nazwa_pliku="klienci_krakow.csv", liczba_osob=10):
    naglowki = ['imie nazwisko', 'adres', 'telefon', 'email', 'link do zdjecia']

    try:
        with open(nazwa_pliku, mode='w', newline='', encoding='utf-8') as plik:
            writer = csv.DictWriter(plik, fieldnames=naglowki)
            writer.writeheader()

            for _ in range(liczba_osob):
                random_id = fake.random_int(min=1, max=1000)

                wiersz = {
                    'imie nazwisko': fake.name(),
                    'adres': generuj_krakowski_adres(),
                    'telefon': fake.phone_number(),
                    'email': fake.email(),
                    'link do zdjecia': f"https://i.pravatar.cc/150?u={random_id}"
                }

                writer.writerow(wiersz)

        print(f"Sukces! Wygenerowano {liczba_osob} profilów z Krakowa w pliku: {nazwa_pliku}")

    except IOError as e:
        print(f"Wystąpił błąd podczas zapisu pliku: {e}")


app = FastAPI(
    title="Providers and Clients API",
    description="API do zarządzania usługodawcami i klientami",
    version="1.0.0"
)

# Lista dozwolonych źródeł
origins = [
    "http://localhost:5173",  # Adres, pod którym działa 'web'
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów z prefiksem /api/v1
app.include_router(api_router, prefix="/api/v1")

# Endpoint startowy
@app.get("/")
def root():
    return {"message": "Witaj w API! Dokumentacja dostępna pod /docs"}

#if __name__ == "__main__":
#    generuj_i_zapisz_do_csv()