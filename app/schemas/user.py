from pydantic import BaseModel
from typing import Optional


# Базовая схема пользователя
class UserBase(BaseModel):
    username: str
    email: str


# Схема для создания пользователя
class UserCreate(UserBase):
    pass


# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


# Схема для ответа клиенту
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True