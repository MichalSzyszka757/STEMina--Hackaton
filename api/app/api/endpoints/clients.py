from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr

# Modele dla Usługobiorcy (Client)
class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class ClientCreate(ClientBase):
    provider_id: Optional[UUID] = None  # Opcjonalne przypisanie do usługodawcy

class Client(ClientBase):
    id: UUID
    provider_id: Optional[UUID] = None


clients_db: List[Client] = []

# --- 4. ENDPOINTY - USŁUGOBIORCY ---
router = APIRouter()

@router.get("/", response_model=List[Client])
def get_clients(provider_id: Optional[UUID] = None):
    # Opcjonalne filtrowanie klientów po ID usługodawcy
    if provider_id:
        return [c for c in clients_db if c.provider_id == provider_id]
    return clients_db

@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate):
    # (Opcjonalnie) Sprawdzenie czy usługodawca istnieje, jeśli podano ID
    if client.provider_id:
         if not any(p.id == client.provider_id for p in providers_db):
             raise HTTPException(status_code=400, detail="Podany ID usługodawcy nie istnieje")

    new_client = Client(
        id=uuid4(),
        **client.dict()
    )
    clients_db.append(new_client)
    return new_client

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: UUID):
    client = next((c for c in clients_db if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: UUID):
    client = next((c for c in clients_db if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")
    clients_db.remove(client)
    return None