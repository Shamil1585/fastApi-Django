# Импорт необходимых модулей
from fastapi import FastAPI
from sqlalchemy import text
from app.database import async_session_maker, Base, engine
from app.routers import categories_router, locations_router, posts_router, comments_router, users_router

# Инициализация приложения FastAPI
app = FastAPI(
    title="Blog API",
    description="Migrated from Django to FastAPI",
    version="1.0.0"
)

# Подключение роутеров (эндпоинтов)
app.include_router(categories_router)
app.include_router(locations_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(users_router)


# Создание таблиц в БД при запуске приложения
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Корневой эндпоинт (главная страница)
@app.get("/")
async def root():
    return {"message": "Blog API is running"}


# Эндпоинт проверки здоровья сервиса
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Эндпоинт проверки подключения к базе данных
@app.get("/db-check")
async def check_database():
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}