from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from typing import Optional, Self
from datetime import datetime


class PostBase(BaseModel):
    """Базовые поля поста — без валидации (для наследования)"""
    title: str
    text: str
    pub_date: datetime
    is_published: bool | None = True
    image: str | None = None
    author_id: int
    location_id: int | None = None
    category_id: int | None = None
    rating: int | None = 0


class PostCreate(PostBase):
    """Схема для создания поста — СТРОГАЯ ВАЛИДАЦИЯ"""
    
    
    title: str = Field(..., min_length=3, max_length=256, description="Заголовок поста (3-256 символов)")
    text: str = Field(..., min_length=10, description="Текст поста (минимум 10 символов)")
    
    author_id: int | None = Field(None, gt=0, description="ID автора (должен существовать)")
    
    location_id: int | None = Field(None, ge=0, description="ID местоположения")
    category_id: int | None = Field(None, ge=0, description="ID категории")
    rating: int | None = Field(0, ge=0, le=10, description="Рейтинг поста (0-10)")
    
    @field_validator('title')
    @classmethod
    def title_not_just_spaces(cls, v: str) -> str:
        """Проверка: заголовок не должен состоять только из пробелов"""
        if not v or not v.strip():
            raise ValueError('Заголовок не может быть пустым или состоять только из пробелов')
        return v.strip()
    
    @field_validator('text')
    @classmethod
    def text_has_words(cls, v: str) -> str:
        """Проверка: текст должен содержать хотя бы одно слово"""
        if not v or not v.strip() or len(v.split()) < 1:
            raise ValueError('Текст поста должен содержать хотя бы одно слово')
        return v.strip()
    
    @field_validator('rating')
    @classmethod
    def rating_must_be_valid(cls, v: int | None) -> int | None:
        """Проверка: рейтинг в диапазоне 0-10"""
        if v is not None and (v < 0 or v > 10):
            raise ValueError('Рейтинг должен быть от 0 до 10')
        return v
    
    @field_validator('image')
    @classmethod
    def image_must_be_url(cls, v: str | None) -> str | None:
        """Проверка: если изображение указано, это должен быть валидный URL"""
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('Изображение должно быть валидным URL (http/https)')
        return v
    
    
    @model_validator(mode='after')
    def validate_pub_date_not_in_future(self) -> Self:
        """Проверка: дата публикации не должна быть в далёком будущем"""
        if self.pub_date and self.pub_date.year > 2030:
            raise ValueError('Дата публикации не должна быть в далёком будущем')
        return self


class PostUpdate(BaseModel):
    """Схема для обновления поста — валидация только изменяемых полей"""
    
    title: str | None = Field(None, min_length=3, max_length=256)
    text: str | None = Field(None, min_length=10)
    pub_date: datetime | None = None
    is_published: bool | None = None
    image: str | None = Field(None, max_length=256)
    location_id: int | None = Field(None, ge=0)
    category_id: int | None = Field(None, ge=0)
    rating: int | None = Field(None, ge=0, le=10)
    
    @field_validator('title')
    @classmethod
    def title_not_just_spaces(cls, v: str | None) -> str | None:
        if v is not None and (not v.strip() if v else False):
            raise ValueError('Заголовок не может быть пустым')
        return v.strip() if v else v
    
    @field_validator('text')
    @classmethod
    def text_has_words(cls, v: str | None) -> str | None:
        if v is not None and (not v.strip() or len(v.split()) < 1 if v else False):
            raise ValueError('Текст должен содержать хотя бы одно слово')
        return v.strip() if v else v


class PostResponse(PostBase):
    """Схема ответа — БЕЗ ВАЛИДАЦИИ (только типы, чтение из БД)"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)