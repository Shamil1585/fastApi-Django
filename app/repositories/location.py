from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.location import Location
from app.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    """Репозиторий для работы с местоположениями"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Location, session)
    
    async def get_published(self) -> list[Location]:
        """Получить только опубликованные местоположения"""
        result = await self.session.execute(
            select(Location).where(Location.is_published == True)
        )
        return result.scalars().all()