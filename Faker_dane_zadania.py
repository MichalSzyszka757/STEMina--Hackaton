import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Inicjalizacja Fakera (potrzebny do generowania numerów budynków i zdań)
fake = Faker('pl_PL')

# Konfiguracja kategorii usług
USLUGI_CONFIG = {
    "Naprawa hydrauliczna": {
        "opisy": ["Cieknący kran w kuchni", "Wymiana rur w łazience", "Montaż nowej baterii wannowej",
                  "Udrożnienie odpływu"],
        "cena_min": 150, "cena_max": 800
    },
    "Pieczenie tortu": {
        "opisy": ["Tort urodzinowy dla dziecka", "Tort piętrowy na wesele", "Wypieki bezglutenowe",
                  "Tort czekoladowy z owocami"],
        "cena_min": 200, "cena_max": 600
    },
    "Kwiaty na okazję": {
        "opisy": ["Bukiet na rocznicę ślubu", "Dekoracja kwiatowa sali", "Pudełko kwiatowe (flowerbox)",
                  "Wiązanka urodzinowa"],
        "cena_min": 80, "cena_max": 400
    },
    "Remont i budowa": {
        "opisy": ["Malowanie pokoju 20m2", "Układanie paneli podłogowych", "Montaż mebli kuchennych",
                  "Gipsowanie ścian"],
        "cena_min": 500, "cena_max": 5000
    }
}


def generuj_zlecenia_bez_klienta(liczba_zadan=10):
    zadania = []
    dostepnosci = ["Od zaraz", "Do uzgodnienia", "Za tydzień"]

    for _ in range(liczba_zadan):
        kategoria = random.choice(list(USLUGI_CONFIG.keys()))
        config = USLUGI_CONFIG[kategoria]

        # Generowanie daty wykonania
        termin = datetime.now() + timedelta(days=random.randint(1, 30))

        zadanie = {
            'Typ usługi': kategoria,
            'Szczegóły': random.choice(config['opisy']),
            'Widełki cenowe': f"{config['cena_min']}-{config['cena_max']} PLN",
            'Wymagana dostępność': random.choice(dostepnosci),
            'Termin wykonania': termin.strftime("%d-%m-%Y"),
            'Zasięg usługi': f"{random.randint(0, 30)} km"
        }
        zadania.append(zadanie)
    return zadania


def zapisz_zlecenia_do_csv(dane, nazwa_pliku="zadania_rynkowe.csv"):
    if not dane: return

    naglowki = ['Typ usługi', 'Widełki cenowe', 'Wymagana dostępność', 'Termin wykonania', 'Szczegóły', 'Zasięg usługi']

    try:
        with open(nazwa_pliku, mode='w', newline='', encoding='utf-8') as plik:
            writer = csv.DictWriter(plik, fieldnames=naglowki)
            writer.writeheader()
            writer.writerows(dane)
        print(f"Pomyślnie wygenerowano plik: {nazwa_pliku}")
    except IOError as e:
        print(f"Błąd zapisu: {e}")


if __name__ == "__main__":
    lista_zadan = generuj_zlecenia_bez_klienta(10)
    zapisz_zlecenia_do_csv(lista_zadan)