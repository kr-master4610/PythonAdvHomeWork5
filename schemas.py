from pydantic import BaseModel, Field
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    answer: str

class QuestionCreate(QuestionBase):
    category_id: int

class QuestionResponse(QuestionBase):
    id: int
    category: Optional[CategoryResponse]
    class Config:
        from_attributes = True