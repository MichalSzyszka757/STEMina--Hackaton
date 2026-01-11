import csv
import random
from faker import Faker

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


if __name__ == "__main__":
    generuj_i_zapisz_do_csv()