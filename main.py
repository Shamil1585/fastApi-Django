import logging
import sys
from fastapi import FastAPI
from app.database import engine
from app.routers import categories, locations, users, posts, comments, auth 
from app.exceptions.handlers import register_exception_handlers
from app.exceptions.validation import register_validation_handler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Blog API",
    description="FastAPI Blog with JWT Authentication",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(auth.router) 
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


register_exception_handlers(app)
register_validation_handler(app) 

@app.get("/")
async def root():
    return {"message": "Blog API with JWT Auth is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}