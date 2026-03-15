from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories import (
    CategoryRepository,
    LocationRepository,
    UserRepository,
    PostRepository,
    CommentRepository,
)


async def get_category_repo(
    db: AsyncSession = Depends(get_db)
) -> CategoryRepository:
    """Зависимость для получения CategoryRepository"""
    return CategoryRepository(session=db)


async def get_location_repo(
    db: AsyncSession = Depends(get_db)
) -> LocationRepository:
    """Зависимость для получения LocationRepository"""
    return LocationRepository(session=db)


async def get_user_repo(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Зависимость для получения UserRepository"""
    return UserRepository(session=db)


async def get_post_repo(
    db: AsyncSession = Depends(get_db)
) -> PostRepository:
    """Зависимость для получения PostRepository"""
    return PostRepository(session=db)


async def get_comment_repo(
    db: AsyncSession = Depends(get_db)
) -> CommentRepository:
    """Зависимость для получения CommentRepository"""
    return CommentRepository(session=db)