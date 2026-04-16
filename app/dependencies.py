from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories import (
    CategoryRepository, LocationRepository, 
    UserRepository, PostRepository, CommentRepository
)
from app.core.security import verify_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_category_repo(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(session=db)

async def get_location_repo(db: AsyncSession = Depends(get_db)) -> LocationRepository:
    return LocationRepository(session=db)

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)

async def get_post_repo(db: AsyncSession = Depends(get_db)) -> PostRepository:
    return PostRepository(session=db)

async def get_comment_repo(db: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session=db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repo)
) -> User:
    """Получить текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail={"message": "Неверные учетные данные"},
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception
    
    username = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = await repo.get_by_username(username)
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user