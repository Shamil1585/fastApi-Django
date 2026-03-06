from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Базовая схема местоположения
class LocationBase(BaseModel):
    name: str
    is_published: bool = True


# Схема для создания местоположения
class LocationCreate(LocationBase):
    pass


# Схема для обновления местоположения
class LocationUpdate(BaseModel):
    name: Optional[str] = None
    is_published: Optional[bool] = None


# Схема для ответа клиенту
class LocationResponse(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True