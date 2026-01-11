import sys
import os
import json
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import class_mapper

# Dodajemy bieżący katalog do ścieżki, by Python widział moduł 'app'
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.provider import Provider
from app.models.task import Task

# --- Konfiguracja Ścieżek ---
# Zakładamy, że folder 'web' jest obok folderu 'api'
# Dostosuj tę ścieżkę, jeśli struktura Twoich folderów jest inna
OUTPUT_DIR = os.path.join(os.getcwd(), "../web/src/data")


def model_to_dict(obj):
    """
    Pomocnicza funkcja zamieniająca obiekt SQLAlchemy na słownik.
    Filtruje pola prywatne (zaczynające się od '_').
    """
    columns = [c.key for c in class_mapper(obj.__class__).columns]
    data = {}
    for c in columns:
        # Pomijamy hasło dla bezpieczeństwa
        if c == "hashed_password":
            continue
        val = getattr(obj, c)

        # Konwersja typów, których JSON nie lubi (UUID, Datetime)
        if isinstance(val, UUID):
            val = str(val)
        elif isinstance(val, datetime):
            val = val.isoformat()

        data[c] = val
    return data


def save_js_file(filename, variable_name, data):
    """
    Zapisuje listę słowników do pliku .js w formacie:
    export const variable_name = [ ... ];
    """
    # Tworzymy pełną ścieżkę do pliku
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Serializacja do JSON z wcięciami
    json_content = json.dumps(data, indent=2, ensure_ascii=False)

    # Treść pliku JS
    js_content = f"export const {variable_name} = {json_content};\n"

    try:
        # Zapis do pliku
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"✅ Zapisano: {filepath}")
    except FileNotFoundError:
        print(f"❌ Błąd: Nie znaleziono katalogu '{OUTPUT_DIR}'. Sprawdź ścieżkę!")


def main():
    db = SessionLocal()
    try:
        print("--- [START] Eksport danych do Frontendu ---")

        # 1. Pobieramy Providerów
        # Filtrujemy tylko tych z rolą PROVIDER
        providers_db = db.query(Provider).filter(Provider.role == "PROVIDER").all()
        # Zamieniamy obiekty na słowniki
        provider_data = [model_to_dict(p) for p in providers_db]

        # 2. Pobieramy Zadania
        tasks_db = db.query(Task).all()
        task_data = [model_to_dict(t) for t in tasks_db]

        # 3. Zapisujemy do plików .js w folderze web
        save_js_file("providerData.js", "providerData", provider_data)
        save_js_file("taskData.js", "taskData", task_data)

        print("--- [KONIEC] Dane zaktualizowane pomyślnie ---")

    finally:
        db.close()


if __name__ == "__main__":
    main()