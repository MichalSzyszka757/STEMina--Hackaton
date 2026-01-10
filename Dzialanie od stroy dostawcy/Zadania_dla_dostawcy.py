import csv
import random
import requests
from datetime import datetime, timedelta

# Rozszerzona lista ID dla każdej kategorii (kilka opcji na wypadek 404)
ZDJECIA_ID_POOL = {
    "Hydrauliczna": ["1584622650111-993a426fbf0a", "1504148455328-c376907d081c", "1607472586893-edb57bdc0e39"],
    "Budowlana": ["1541888941-2c02d2970c31", "1504307651254-35680f356dfd", "1590644365607-1c5a519a7a37"],
    "Florystyczna": ["1526047932273-341f2a7631f9", "1490750967868-88aa4486c946", "1519340333755-56e9c1d04579"],
    "Dentystyczna": ["1606811841689-23dfddce3e95", "1588776814546-1ffcf47267a5", "1598256989800-fe5f95da9787"],
    "Elektryczna": ["1621905251189-08b45d6a269e", "1558210834-473f430c09ac", "1473341304179-c151f055318a"],
    "IT i Grafika": ["1517694712202-14dd9538aa97", "1555066931-4365d14bab8c", "1586717791821-3f44a563eb4c"],
    "Transport i Przeprowadzki": ["1586749835756-37352135ed36", "1600518464441-9154a4dba221",
                                  "1520641328444-539ad5be9102"],
    "Ogrody i Tereny Zielone": ["1585320806297-9794b3e4eeae", "1592419044706-39796d40f98c", "1558904541-df4a7df93d67"],
    "Motoryzacyjna": ["1486006396193-47106858e74a", "1487754180451-c456f719a1fc", "1530046339160-ce3e530c7d2f"],
    "Uroda i Relaks": ["1540555700478-4be289fbecee", "1515377905703-c4788e51af15", "1512290923902-8a9f81dc206e"],
    "Sprzątająca": ["1581578731522-745d05cb9724", "1528740561666-dc2479dc08ab", "1584622781564-1d987f7333c1"],
    "Korepetycje i Edukacja": ["1434030216411-0b793f4b4173", "1503676260728-1c00da094a0b",
                               "1497633762264-8ad2ee358a72"],
    "Naprawa Urządzeń": ["1597733336794-12d05021d510", "1517077304055-6e89abbf09b0", "1581093148114-1e715690a3f5"]
}

DEFAULT_PHOTO = "1521737711867-e3b97375f902"

# Podręczna pamięć (cache) aby nie sprawdzać tego samego zdjęcia 1000 razy
sprawdzone_linki = {}


def sprawdz_i_pobierz_link(kategoria):
    """Wybiera ID, sprawdza czy nie zwraca 404 i zwraca gotowy link."""
    pool = ZDJECIA_ID_POOL.get(kategoria, [DEFAULT_PHOTO])
    random.shuffle(pool)  # Losowa kolejność sprawdzania

    for photo_id in pool:
        # Jeśli już sprawdzaliśmy to ID, zwróć wynik z pamięci
        if photo_id in sprawdzone_linki:
            if sprawdzone_linki[photo_id] is not None:
                return sprawdzone_linki[photo_id]
            continue

        url = f"https://images.unsplash.com/photo-{photo_id}?q=80&w=800&auto=format&fit=crop"

        try:
            # requests.head jest szybszy niż .get, bo nie pobiera obrazka, tylko nagłówki
            response = requests.head(url, timeout=3)
            if response.status_code == 200:
                sprawdzone_linki[photo_id] = url
                return url
            else:
                print(f"Błąd {response.status_code} dla {photo_id}. Szukam dalej...")
                sprawdzone_linki[photo_id] = None
        except:
            sprawdzone_linki[photo_id] = None

    # Jeśli wszystko zawiedzie, używamy placeholder
    return f"https://placehold.co/600x400?text={kategoria.replace(' ', '+')}"


def generuj_bezpieczna_baze(liczba_rekordow=1000):
    konfiguracja = []
    try:
        with open("konfiguracja_uslug.csv", mode='r', encoding='utf-8') as plik:
            reader = csv.DictReader(plik)
            konfiguracja = [row for row in reader]
    except FileNotFoundError:
        print("Najpierw przygotuj plik konfiguracja_uslug.csv!")
        return

    try:
        with open("baza_zadan.csv", mode='w', newline='', encoding='utf-8') as f_csv, \
                open("baza_zadan.sql", mode='w', encoding='utf-8') as f_sql:

            writer = csv.DictWriter(f_csv,
                                    fieldnames=['Typ usługi', 'Rodzaj usługi (Budżet)', 'Odległość', 'Termin wykonania',
                                                'Opis zadania', 'Link do zdjęcia'])
            writer.writeheader()

            f_sql.write("BEGIN TRANSACTION;\n")
            f_sql.write(
                "CREATE TABLE IF NOT EXISTS zadania (id INTEGER PRIMARY KEY AUTOINCREMENT, typ_uslugi TEXT, budzet TEXT, odleglosc TEXT, termin DATE, opis TEXT, zdjecie_url TEXT);\n")

            print("Rozpoczynam generowanie i weryfikację zdjęć...")

            for i in range(liczba_rekordow):
                szablon = random.choice(konfiguracja)
                typ = szablon['Typ']

                # Funkcja sprawdzająca linki przed zapisem
                zdjecie_url = sprawdz_i_pobierz_link(typ)

                odleglosc = f"{random.randint(1, 30)} km"
                termin = (datetime.now() + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")

                # CSV
                writer.writerow({
                    'Typ usługi': typ, 'Rodzaj usługi (Budżet)': szablon['Budzet'], 'Odległość': odleglosc,
                    'Termin wykonania': termin, 'Opis zadania': szablon['Opis'], 'Link do zdjęcia': zdjecie_url
                })

                # SQL (zmienne pomocnicze dla czystości kodu i uniknięcia SyntaxError)
                c_typ = typ.replace("'", "''")
                c_budzet = szablon['Budzet']
                c_opis = szablon['Opis'].replace("'", "''")

                sql_line = f"INSERT INTO zadania (typ_uslugi, budzet, odleglosc, termin, opis, zdjecie_url) VALUES ('{c_typ}', '{c_budzet}', '{odleglosc}', '{termin}', '{c_opis}', '{zdjecie_url}');\n"
                f_sql.write(sql_line)

                if (i + 1) % 100 == 0:
                    print(f"Przetworzono {i + 1} rekordów...")

            f_sql.write("COMMIT;")

        print("Sukces! Wygenerowano pliki z przetestowanymi linkami.")

    except Exception as e:
        print(f"Błąd krytyczny: {e}")


if __name__ == "__main__":
    generuj_bezpieczna_baze()