from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
from typing import AsyncGenerator


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

# Создание асинхронного движка
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Логирование SQL-запросов (для отладки)
)

# Сессия для работы с БД
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()


# Функция для получения сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий базы данных.
    Используется в зависимостях FastAPI.
    """
    async with async_session_maker() as session:
        yield session