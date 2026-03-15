from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
    
    async def get_by_slug(self, slug: str) -> Category | None:
        """Получить категорию по slug"""
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()
    
    async def get_published(self) -> list[Category]:
        """Получить только опубликованные категории"""
        result = await self.session.execute(
            select(Category).where(Category.is_published == True)
        )
        return result.scalars().all()