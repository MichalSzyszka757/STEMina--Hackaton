from fastapi import APIRouter, Depends, status
from typing import List, Optional, Annotated
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

from app.schemas.user import User
from app.core.auth import get_current_user

class TaskStatus(str, Enum):
    OPEN = "OPEN"           # Czeka na wykonawcę
    ASSIGNED = "ASSIGNED"   # Wykonawca przypisany
    COMPLETED = "COMPLETED" # Zakończone

class TaskBudget(str, Enum):
    BUDGET = "BUDGET"
    STANDARD = "STANDARD"

class TaskBase(BaseModel):
    category: str        # np. "IT", "Hydraulik" - to musi pasować do usług providera
    title: str
    details: str
    budget: TaskBudget
    distance: int
    deadline: datetime

class TaskCreate(TaskBase):
    client_id: UUID      # Kto zleca

class Task(TaskBase):
    id: UUID
    client_id: UUID
    provider_id: Optional[UUID] = None # Kto wykonuje (puste na początku)
    status: TaskStatus = TaskStatus.OPEN

router = APIRouter()

# @router.get("/")
# def get_tasks():
    
#     return [Task(id=uuid4(), test_field=1, test_field2=2), Task(id=uuid4(), test_field=2, test_field2=3)]
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def read_user_me(
    task: TaskBase,
    current_user: Annotated[User, Depends(get_current_user)]
):
    print(user)
    return task

#@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
#def create_task(task: TaskBase):
#    return task

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

@router.post("/{task_id}/applications")
def apply_for_task(task_id: UUID):
    """
    Provider zgłasza się, a Klient wybiera z listy chętnych.
    """
    return None