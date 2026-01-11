from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated
from uuid import UUID
from sqlalchemy.orm import Session

# Importy systemowe
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User, UserRole
from app.models.task import Task
from app.models.provider import Provider

# Importy schematów (DTO)
from app.schemas.task import TaskResponse, CreateTask  # Upewnij się, że masz CreateTask w schemas
from app.schemas.provider import ProviderResponse

# Import logiki matchowania
from app.services.matching_service import find_matches_for_task

router = APIRouter()


# --- 1. TWORZENIE ZADANIA (Przez Klienta) ---
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
        task_in: CreateTask,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Klient tworzy nowe zadanie.
    Automatycznie przypisujemy ID zalogowanego użytkownika jako client_id.
    """
    # Zabezpieczenie: Tylko KLIENT może tworzyć zadania
    if current_user.role != UserRole.CLIENT:
        raise HTTPException(status_code=403, detail="Tylko klienci mogą tworzyć zadania")

    # Konwersja schematu Pydantic na model SQLAlchemy
    new_task = Task(
        **task_in.model_dump(),
        client_id=current_user.id,  # Przypisanie właściciela
        status="OPEN"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# --- 2. FEED (Pobranie pasujących kart) ---
@router.get("/{task_id}/matches", response_model=List[ProviderResponse])
def get_task_matches(
        task_id: UUID,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Wyświetla listę pasujących Providerów dla danego zadania.
    To są 'karty', które widzi Klient (lub Providerzy widzą zadanie).
    """
    # Sprawdzenie czy zadanie istnieje
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")

    # Użycie serwisu matchującego (z poprzednich kroków)
    return find_matches_for_task(db, task.id)


# --- 3. SWIPE RIGHT (Provider aplikuje do zadania) ---
@router.post("/{task_id}/apply", status_code=status.HTTP_200_OK)
def apply_for_task(
        task_id: UUID,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    """
    AKCJA SWIPE RIGHT PRZEZ PROVIDERA.
    Provider zgłasza chęć wykonania zadania.
    """
    # 1. Sprawdź czy user to Provider
    if current_user.role != UserRole.PROVIDER:
        raise HTTPException(status_code=403, detail="Tylko Provider może aplikować")

    # 2. Pobierz zadanie
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")

    # 3. Pobierz obiekt Providera (rzutowanie User -> Provider)
    # W SQLAlchemy, jeśli używasz dziedziczenia, current_user powinien mieć dostęp do pól Providera
    # lub musimy go pobrać z tabeli providers.
    provider = db.query(Provider).filter(Provider.id == current_user.id).first()

    # 4. Dodaj do kandydatów (Relacja Many-to-Many)
    if provider not in task.candidates:
        task.candidates.append(provider)
        db.commit()
        return {"message": "Aplikacja wysłana (Swipe Right udany)"}
    else:
        return {"message": "Już aplikowałeś do tego zadania"}


# --- 4. MATCH (Klient akceptuje Providera) ---
@router.post("/{task_id}/accept/{provider_id}", response_model=TaskResponse)
def accept_provider(
        task_id: UUID,
        provider_id: UUID,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    """
    AKCJA SWIPE RIGHT PRZEZ KLIENTA.
    Klient wybiera konkretnego Providera z listy kandydatów -> MATCH.
    """
    task = db.query(Task).filter(Task.id == task_id).first()

    # Security: Czy to zadanie należy do tego klienta?
    if task.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="To nie Twoje zadanie")

    # Sprawdź czy ten provider faktycznie aplikował
    selected_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if selected_provider not in task.candidates:
        raise HTTPException(status_code=400, detail="Ten provider nie zgłosił się do zadania")

    # --- LOGIKA MATCHU ---
    task.provider_id = selected_provider.id  # Przypisz wykonawcę
    task.status = "ASSIGNED"  # Zmień status

    # Tutaj można dodać logikę tworzenia czatu w przyszłości
    # create_chat_room(task.client_id, selected_provider.id)

    db.commit()
    db.refresh(task)

    return task


# --- 5. Pobieranie szczegółów i usuwanie (Standardowy CRUD) ---

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: Annotated[Session, Depends(get_db)]):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: UUID,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")

    # Security: Tylko właściciel może usunąć
    if task.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nie możesz usunąć cudzego zadania")

    db.delete(task)
    db.commit()
    return None