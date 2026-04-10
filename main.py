from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine
from app.routers import categories, locations, users, posts, comments
from app.exceptions import AppException

app = FastAPI(
    title="Blog API",
    description="Migrated from Django to FastAPI",
    version="1.0.0"
)


# === Глобальный обработчик кастомных исключений ===
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Единый формат ошибок для всех кастомных исключений"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


# Подключаем роутеры
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
async def root():
    return {"message": "Blog API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/db-check")
async def db_check():
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}