from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения — ВСЕ поля со значениями по умолчанию!"""
    
    # === База данных ===
    DATABASE_URL: str = "sqlite+aiosqlite:///./blog.db"  
    
    # === JWT настройки ===
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # === Приложение ===
    APP_NAME: str = "Blog API"
    DEBUG: bool = True
    
    # === Настройки Pydantic ===
    class Config:
        env_file = ".env"
        extra = "allow"


# Глобальный экземпляр
settings = Settings()