import csv
import random
from datetime import datetime, timedelta


def wczytaj_konfiguracje(nazwa_pliku="USLUGI_CONFIG.csv"):
    config = {}
    try:
        with open(nazwa_pliku, mode='r', encoding='utf-8') as plik:
            reader = list(csv.reader(plik))
            if not reader:
                return config

            # Nagłówki to typy usług (wiersz 0)
            typy_uslug = reader[0]

            for i, typ in enumerate(typy_uslug):
                # Cena min (wiersz 1), Cena max (wiersz 2)
                cena_min = int(reader[1][i])
                cena_max = int(reader[2][i])

                # Opisy to wszystkie wiersze od 3 w dół dla danej kolumny
                # Filtrujemy puste komórki, jeśli kolumny mają różną liczbę opisów
                opisy = [row[i] for row in reader[3:] if i < len(row) and row[i].strip()]

                config[typ] = {
                    "opisy": opisy,
                    "cena_min": cena_min,
                    "cena_max": cena_max
                }
        return config
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}")
        return {}
    except ValueError:
        print("Błąd: Sprawdź czy ceny w 2 i 3 wierszu są liczbami.")
        return {}


def generuj_zlecenia_z_csv(liczba_zadan=10):
    config = wczytaj_konfiguracje()
    if not config:
        return

    zadania = []
    typy = list(config.keys())
    dostepnosci = ["Od zaraz", "Do uzgodnienia", "Za tydzień"]

    for _ in range(liczba_zadan):
        typ = random.choice(typy)
        c = config[typ]

        termin = datetime.now() + timedelta(days=random.randint(1, 30))

        zadanie = {
            'Typ usługi': typ,
            'Widełki cenowe': f"{c['cena_min']}-{c['cena_max']} PLN",
            'Wymagana dostępność': random.choice(dostepnosci),
            'Termin wykonania': termin.strftime("%d-%m-%Y"),
            'Szczegóły': random.choice(c['opisy']),
            'Zasięg usługi': f"{random.randint(0, 30)} km"
        }
        zadania.append(zadanie)

    return zadania


def zapisz_wynik(dane, nazwa_pliku="wygenerowane_zadania.csv"):
    if not dane: return
    naglowki = dane[0].keys()
    with open(nazwa_pliku, mode='w', newline='', encoding='utf-8') as plik:
        writer = csv.DictWriter(plik, fieldnames=naglowki)
        writer.writeheader()
        writer.writerows(dane)
    print(f"Pomyślnie wygenerowano {len(dane)} zadań na podstawie pliku CSV.")


if __name__ == "__main__":
    wynik = generuj_zlecenia_z_csv(10)
    zapisz_wynik(wynik)