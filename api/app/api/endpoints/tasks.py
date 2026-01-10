from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

class TaskBase(BaseModel):
    test_field: int
    test_field2: int

class Task(TaskBase):
    id: UUID
    # provider_id: Optional[UUID] = None

router = APIRouter()

@router.get("/")
def get_tasks():
    
    return [Task(id=uuid4(), test_field=1, test_field2=2), Task(id=uuid4(), test_field=2, test_field2=3)]

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(client: TaskBase):
    
    # new_client = Client(
    #     id=uuid4(),
    #     **client.dict()
    # )
    # clients_db.append(new_client)
    return Task(test_field=3, test_field2=4)

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    #client = next((c for c in clients_db if c.id == client_id), None)
    #if not client:
    #    raise HTTPException(status_code=404, detail="Klient nie znaleziony")
    return Task(test_field=1, test_field2=2)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    # client = next((c for c in clients_db if c.id == client_id), None)
    # if not client:
    #     raise HTTPException(status_code=404, detail="Klient nie znaleziony")
    # clients_db.remove(client)
    return None