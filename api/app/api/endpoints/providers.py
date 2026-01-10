from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import List, Optional

# Modele dla Usługodawcy (Provider)
class ProviderBase(BaseModel):
    name: str
    tax_id: str  # np. NIP
    email: EmailStr
    city: str

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None

class Provider(ProviderBase):
    id: UUID
    is_active: bool = True

providers_db: List[Provider] = []

# --- 3. ENDPOINTY - USŁUGODAWCY ---
router = APIRouter()

@router.get("/", response_model=List[Provider])
def get_providers():
    return providers_db

@router.post("/", response_model=Provider, status_code=status.HTTP_201_CREATED)
def create_provider(provider: ProviderCreate):
    new_provider = Provider(
        id=uuid4(),
        **provider.dict()
    )
    providers_db.append(new_provider)
    return new_provider

@router.get("/{provider_id}", response_model=Provider)
def get_provider(provider_id: UUID):
    # Szukanie w liście (symulacja zapytania SQL)
    provider = next((p for p in providers_db if p.id == provider_id), None)
    if not provider:
        raise HTTPException(status_code=404, detail="Usługodawca nie znaleziony")
    return provider

@router.patch("/{provider_id}", response_model=Provider)
def update_provider(provider_id: UUID, provider_update: ProviderUpdate):
    stored_provider = next((p for p in providers_db if p.id == provider_id), None)
    if not stored_provider:
        raise HTTPException(status_code=404, detail="Usługodawca nie znaleziony")
    
    # Aktualizacja tylko przesłanych pól
    update_data = provider_update.dict(exclude_unset=True)
    updated_provider = stored_provider.copy(update=update_data)
    
    # Podmiana w "bazie"
    index = providers_db.index(stored_provider)
    providers_db[index] = updated_provider
    
    return updated_provider

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(provider_id: UUID):
    provider = next((p for p in providers_db if p.id == provider_id), None)
    if not provider:
        raise HTTPException(status_code=404, detail="Usługodawca nie znaleziony")
    providers_db.remove(provider)
    return None

@router.get("/{provider_id}/opportunities")
def provider_opportunities():
    """
    Logika: Backend sprawdza: "Jakie specjalizacje ma ten provider?" -> "Znajdź wolne zadania w tych kategoriach".

    To jest Twój "feed" dla wykonawcy.
    """
    return None

