from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Базовая схема категории
class CategoryBase(BaseModel):
    title: str
    description: str
    slug: str
    is_published: bool = True


# Схема для создания категории
class CategoryCreate(CategoryBase):
    pass


# Схема для обновления категории (все поля необязательны)
class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None


# Схема для ответа клиенту
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Разрешить чтение из SQLAlchemy моделей