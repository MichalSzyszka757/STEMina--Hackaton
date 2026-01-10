import requests

# --- GOOGLE PLACES ---
def get_places_data(api_key, query):
    """
    Pobiera dane firm z Google Places API (New).
    """
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types"
    }
    data = {"textQuery": query}

    # Wysłanie żądania POST
    response = requests.post(url, headers=headers, json=data)

    # Sprawdzenie statusu odpowiedzi
    if response.status_code == 200:
        results = response.json().get('places', [])

        # Iteracja po znalezionych miejscach
        for place in results:
            name = place.get('displayName', {}).get('text', 'Brak nazwy')
            address = place.get('formattedAddress', 'Brak adresu')
            types = place.get('types', [])
            print(f"Firma: {name}, Adres: {address}")

    else:
        # Obsługa błędu HTTP
        print(f"Błąd Google: {response.status_code}")


# --- ALLEGRO ---
def search_allegro_companies(access_token, query):
    """
    Szuka ofert firmowych na Allegro.
    """
    url = "https://api.allegro.pl/offers/listing"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.allegro.public.v1+json"
    }
    params = {
        "phrase": query,
        "seller.company": "true",  # Filtr na firmy
        "limit": 10
    }

    # Wysłanie żądania GET
    response = requests.get(url, headers=headers, params=params)

    # Sprawdzenie czy udało się pobrać dane
    if response.status_code == 200:
        items = response.json().get('items', {}).get('regular', [])

        # Pętla po ofertach
        for item in items:
            seller = item.get('seller', {}).get('login', 'Nieznany')
            print(f"Sprzedawca: {seller}")

    else:
        # Logowanie błędu w przypadku niepowodzenia
        print(f"Błąd Allegro: {response.status_code}")


# --- CEIDG (GOV) ---
def get_ceidg_data(api_key, city, pkd_code):
    """
    Pobiera firmy z CEIDG po mieście i PKD.
    """
    url = "https://dane.biznes.gov.pl/api/ceidg/v2/firmy"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "adresDzialalnosci.miasto": city,
        "pkd": pkd_code,
        "limit": 5
    }

    # Wysłanie zapytania GET
    response = requests.get(url, headers=headers, params=params)

    # Weryfikacja poprawności odpowiedzi
    if response.status_code == 200:
        firmy = response.json().get('firmy', [])

        # Iteracja przez listę firm
        for firma in firmy:
            imie = firma.get('wlasciciel', {}).get('imie', '')
            nazwisko = firma.get('wlasciciel', {}).get('nazwisko', '')
            print(f"Firma w CEIDG: {imie} {nazwisko}")

    else:
        # Komunikat o błędzie połączenia
        print(f"Błąd CEIDG: {response.status_code}")