from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr
from faker import Faker

# Inicjalizacja polskiej lokalizacji
fake = Faker('pl_PL')

# Modele dla Usługobiorcy (Client)
class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

# class ClientCreate(ClientBase):
#     provider_id: Optional[UUID] = None  # Opcjonalne przypisanie do usługodawcy

class Client(ClientBase):
    id: UUID
    # provider_id: Optional[UUID] = None


#clients_db: List[Client] = []

# --- 4. ENDPOINTY - USŁUGOBIORCY ---
router = APIRouter()

@router.get("/", response_model=List[Client])
def get_clients():
    clients = []
    for _ in range(20):

        name = fake.name()
        client = Client(id=uuid4(), first_name=name.strip().split()[0], last_name=name.strip().split()[1], email=fake.email())
        #client.id = fake.random_int(min=1, max=1000)
        #client.first_name = name.strip().split()[0]
        #client.last_name = name.strip().split()[1]
        #client.email = fake.email()

        clients.append(client)

    return clients

@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientBase):
    
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