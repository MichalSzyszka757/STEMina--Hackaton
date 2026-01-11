from app.schemas.category import CreateCategory, CategoryResponse
from app.models.category import Category as DbCategory
from app.core.database import SessionDep
from fastapi import APIRouter, status
from typing import List, Annotated

# --- 4. ENDPOINTY - USŁUGOBIORCY ---
router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories():
    return db.query(DbCategory)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(db: SessionDep, category: CreateCategory) -> CategoryResponse:
    obj_data = DbCategory(name=category.name)

    db.add(obj_data)
    db.commit()
    db.refresh(obj_data)

    return CategoryResponse(id=obj_data.id, name=obj_data.name)