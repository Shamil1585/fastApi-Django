from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from app.models.post import Post
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseError, NotFoundException


class PostRepository(BaseRepository[Post]):
    """Репозиторий для работы с постами — с обработкой ошибок БД"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)
    
    async def get_by_id(self, id: int):
        """Получить пост по ID с обработкой ошибок"""
        try:
            result = await self.session.execute(
                select(Post).where(Post.id == id)
            )
            return result.scalar_one_or_none()
        except OperationalError as e:
            # Ошибка подключения к БД
            raise DatabaseError(
                message="Не удалось подключиться к базе данных",
                original_error=str(e)
            )
        except SQLAlchemyError as e:
            # Любая другая ошибка SQLAlchemy
            raise DatabaseError(
                message=f"Ошибка при получении поста с ID {id}",
                original_error=str(e)
            )
    
    async def get_all(self):
        """Получить все посты с обработкой ошибок"""
        try:
            result = await self.session.execute(select(Post))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError(
                message="Ошибка при получении списка постов",
                original_error=str(e)
            )
    
    async def create(self, obj_create):
        """Создать пост с обработкой ошибок"""
        try:
            db_obj = self.model(**obj_create.model_dump())
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await self.session.rollback()
            # Нарушение уникальности или внешних ключей
            if "UNIQUE constraint failed" in str(e):
                raise DatabaseError(
                    message="Нарушение уникальности: такой пост уже существует",
                    original_error=str(e)
                )
            elif "FOREIGN KEY constraint failed" in str(e):
                raise DatabaseError(
                    message="Нарушение внешней ссылки: проверьте author_id, category_id, location_id",
                    original_error=str(e)
                )
            raise DatabaseError(
                message="Ошибка целостности данных при создании поста",
                original_error=str(e)
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError(
                message="Ошибка при создании поста",
                original_error=str(e)
            )
    
    async def update(self, db_obj, obj_update):
        """Обновить пост с обработкой ошибок"""
        try:
            update_data = obj_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError(
                message="Ошибка при обновлении поста",
                original_error=str(e)
            )
    
    async def delete(self, db_obj):
        """Удалить пост с обработкой ошибок"""
        try:
            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError(
                message="Ошибка при удалении поста",
                original_error=str(e)
            )