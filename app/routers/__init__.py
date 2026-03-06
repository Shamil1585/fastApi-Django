# Импорт всех роутеров
from app.routers.categories import router as categories_router
from app.routers.locations import router as locations_router
from app.routers.posts import router as posts_router
from app.routers.comments import router as comments_router

__all__ = ["categories_router", "locations_router", "posts_router", "comments_router"]