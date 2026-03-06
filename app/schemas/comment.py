from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Базовая схема комментария
class CommentBase(BaseModel):
    text: str


# Схема для создания комментария
class CommentCreate(CommentBase):
    author_id: int
    post_id: int


# Схема для обновления комментария
class CommentUpdate(BaseModel):
    text: Optional[str] = None


# Схема для ответа клиенту
class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        from_attributes = True