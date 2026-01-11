from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.provider import Provider
from app.models.enums import get_days_from_lead_time

def find_matches_for_task(db: Session, task_id: int):
    """
    Zwraca listę Providerów pasujących do Zadania.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return []

    # KROK 1: Twarde filtrowanie bazy (SQL)
    # Pobieramy tylko tych z tą samą kategorią i półką cenową
    candidates = db.query(Provider).filter(
        Provider.specialization_id == task.category_id, # Zakładając, że Provider ma jedną główną specjalizację lub logicznie to powiążemy
        Provider.price_tier == task.budget # Budget klienta == PriceTier providera
    ).all()

    matches = []

    # KROK 2: Logika biznesowa (Python)
    task_days = get_days_from_lead_time(task.deadline_limit)

    for provider in candidates:
        # A. Sprawdzenie Dystansu (wartość bezwzględna różnicy lokalizacji)
        # Zakładamy, że location to np. kod pocztowy lub liczba km od centrum
        dist = abs(task.client_location - provider.location)
        if dist > task.max_distance:
            continue

        # B. Sprawdzenie Terminowości
        provider_days = get_days_from_lead_time(provider.lead_time)
        if provider_days > task_days:
            continue

        # Jeśli przeszedł testy -> dodajemy do listy
        matches.append(provider)

    return matches