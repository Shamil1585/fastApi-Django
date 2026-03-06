# Импорт всех схем для удобного доступа
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse

__all__ = [
    "CategoryCreate", "CategoryUpdate", "CategoryResponse",
    "LocationCreate", "LocationUpdate", "LocationResponse",
    "PostCreate", "PostUpdate", "PostResponse",
    "CommentCreate", "CommentUpdate", "CommentResponse",
    "UserCreate", "UserUpdate", "UserResponse"
]