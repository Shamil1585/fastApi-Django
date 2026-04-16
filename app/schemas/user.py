from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr


class UserCreate(UserBase):
    """Схема для регистрации"""
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Минимум 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Нужна заглавная буква')
        if not any(c.isdigit() for c in v):
            raise ValueError('Нужна цифра')
        return v


class UserLogin(BaseModel):
    """Схема для входа"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Схема для обновления"""
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Схема ответа"""
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные из токена"""
    username: Optional[str] = None
    user_id: Optional[int] = None