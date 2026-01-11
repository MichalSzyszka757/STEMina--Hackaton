from pydantic import BaseModel
from uuid import UUID

class CategoryBase(BaseModel):
    name: str


class CreateCategory(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    name: str