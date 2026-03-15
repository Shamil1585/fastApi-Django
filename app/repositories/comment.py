from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.comment import Comment
from app.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    """Репозиторий для работы с комментариями"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)
    
    async def get_by_post(self, post_id: int) -> list[Comment]:
        """Получить все комментарии к посту"""
        result = await self.session.execute(
            select(Comment).where(Comment.post_id == post_id)
        )
        return result.scalars().all()
    
    async def get_by_author(self, author_id: int) -> list[Comment]:
        """Получить все комментарии автора"""
        result = await self.session.execute(
            select(Comment).where(Comment.author_id == author_id)
        )
        return result.scalars().all()