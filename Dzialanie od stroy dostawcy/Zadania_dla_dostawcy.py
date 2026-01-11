import csv
import random
from datetime import datetime, timedelta


def generuj_dane_podwojnie(liczba_rekordow=1000):
    # 1. Wczytanie konfiguracji z pliku CSV
    konfiguracja = []
    try:
        with open("konfiguracja_uslug.csv", mode='r', encoding='utf-8') as plik:
            reader = csv.DictReader(plik)
            konfiguracja = [row for row in reader]
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku 'konfiguracja_uslug.csv'!")
        return

    # Nazwy plików wyjściowych
    plik_csv = "baza_zadan.csv"
    plik_sql = "baza_zadan.sql"

    # Nagłówki dla CSV
    naglowki_csv = ['Typ usługi', 'Rodzaj usługi (Budżet)', 'Odległość', 'Termin wykonania', 'Opis zadania']

    try:
        with open(plik_csv, mode='w', newline='', encoding='utf-8') as f_csv, \
                open(plik_sql, mode='w', encoding='utf-8') as f_sql:

            # Inicjalizacja CSV
            writer = csv.DictWriter(f_csv, fieldnames=naglowki_csv)
            writer.writeheader()

            # Inicjalizacja SQL (Schema)
            f_sql.write("BEGIN TRANSACTION;\n")
            f_sql.write("CREATE TABLE IF NOT EXISTS zadania (\n")
            f_sql.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
            f_sql.write("    typ_uslugi VARCHAR(100),\n")
            f_sql.write("    budzet VARCHAR(50),\n")
            f_sql.write("    odleglosc VARCHAR(20),\n")
            f_sql.write("    termin_wykonania DATE,\n")
            f_sql.write("    opis_zadania TEXT\n")
            f_sql.write(");\n\n")

            for _ in range(liczba_rekordow):
                # Losowanie bazy z konfiguracji
                szablon = random.choice(konfiguracja)

                # Generowanie zmiennych
                typ = szablon['Typ']
                budzet = szablon['Budzet']
                opis = szablon['Opis']
                odleglosc = f"{random.randint(1, 30)} km"

                # Data (Format YYYY-MM-DD - standard dla SQL i Excela)
                data_obj = datetime.now() + timedelta(days=random.randint(0, 60))
                termin = data_obj.strftime("%Y-%m-%d")

                # --- ZAPIS DO CSV ---
                writer.writerow({
                    'Typ usługi': typ,
                    'Rodzaj usługi (Budżet)': budzet,
                    'Odległość': odleglosc,
                    'Termin wykonania': termin,
                    'Opis zadania': opis
                })

                # --- ZAPIS DO SQL ---
                # Czyszczenie apostrofów dla SQL, aby uniknąć błędów składni
                typ_sql = typ.replace("'", "''")
                opis_sql = opis.replace("'", "''")

                sql_line = f"INSERT INTO zadania (typ_uslugi, budzet, odleglosc, termin_wykonania, opis_zadania) " \
                           f"VALUES ('{typ_sql}', '{budzet}', '{odleglosc}', '{termin}', '{opis_sql}');\n"
                f_sql.write(sql_line)

            f_sql.write("\nCOMMIT;")

        print(f"Sukces! Wygenerowano 1000 rekordów.")
        print(f"1. Plik CSV: {plik_csv}")
        print(f"2. Plik SQL: {plik_sql}")

    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    generuj_dane_podwojnie()
