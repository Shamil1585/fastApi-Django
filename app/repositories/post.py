from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.post import Post
from app.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    """Репозиторий для работы с постами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)
    
    async def get_by_author(self, author_id: int) -> list[Post]:
        """Получить все посты автора"""
        result = await self.session.execute(
            select(Post).where(Post.author_id == author_id)
        )
        return result.scalars().all()
    
    async def get_by_category(self, category_id: int) -> list[Post]:
        """Получить посты по категории"""
        result = await self.session.execute(
            select(Post).where(Post.category_id == category_id)
        )
        return result.scalars().all()
    
    async def get_published(self) -> list[Post]:
        """Получить только опубликованные посты"""
        result = await self.session.execute(
            select(Post).where(Post.is_published == True)
        )
        return result.scalars().all()