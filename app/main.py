from fastapi import FastAPI
from sqlalchemy import text
from app.database import async_session_maker, Base, engine

# Инициализация приложения
app = FastAPI(
    title="Blog API",
    description="Migrated from Django to FastAPI",
    version="1.0.0"
)


# Создание таблиц при запуске
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Корневой эндпоинт
@app.get("/")
async def root():
    return {"message": "Blog API is running"}


# Проверка здоровья
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Проверка подключения к БД
@app.get("/db-check")
async def check_database():
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}