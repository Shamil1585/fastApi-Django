from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Базовая схема поста
class PostBase(BaseModel):
    title: str
    text: str
    pub_date: datetime
    is_published: bool = True
    image: Optional[str] = None


# Схема для создания поста
class PostCreate(PostBase):
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None


# Схема для обновления поста
class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None


# Схема для ответа клиенту
class PostResponse(PostBase):
    id: int
    created_at: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True